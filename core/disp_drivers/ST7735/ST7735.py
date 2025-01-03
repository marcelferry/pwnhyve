
import time
import core.disp_drivers.ST7735.config as config

class ST7735(config.RaspberryPi):

    NOP = 0x0
    SWRESET = 0x01
    RDDID = 0x04
    RDDST = 0x09

    SLPIN  = 0x10
    SLPOUT  = 0x11
    PTLON  = 0x12
    NORON  = 0x13

    INVOFF = 0x20
    INVON = 0x21
    DISPOFF = 0x28
    DISPON = 0x29
    CASET = 0x2A
    RASET = 0x2B
    RAMWR = 0x2C
    RAMRD = 0x2E

    VSCRDEF = 0x33
    VSCSAD = 0x37

    COLMOD = 0x3A
    MADCTL = 0x36

    FRMCTR1 = 0xB1
    FRMCTR2 = 0xB2
    FRMCTR3 = 0xB3
    INVCTR = 0xB4
    DISSET5 = 0xB6

    PWCTR1 = 0xC0
    PWCTR2 = 0xC1
    PWCTR3 = 0xC2
    PWCTR4 = 0xC3
    PWCTR5 = 0xC4
    VMCTR1 = 0xC5

    RDID1 = 0xDA
    RDID2 = 0xDB
    RDID3 = 0xDC
    RDID4 = 0xDD

    PWCTR6 = 0xFC

    GMCTRP1 = 0xE0
    GMCTRN1 = 0xE1


    width = 128
    height = 128 

    def command(self, cmd):
        self.digital_write(self.GPIO_DC_PIN, False)
        self.spi_writebyte([cmd])      
    def data(self, val):
        self.digital_write(self.GPIO_DC_PIN, True)
        self.spi_writebyte([val])

    def reset(self):
        """Reset the display"""
        self.digital_write(self.GPIO_RST_PIN,True)
        time.sleep(0.01)
        self.digital_write(self.GPIO_RST_PIN,False)
        time.sleep(0.01)
        self.digital_write(self.GPIO_RST_PIN,True)
        time.sleep(0.01)

    def SetGramScanWay(self, Scan_dir):
        #Get the screen scan direction
        self.LCD_Scan_Dir = Scan_dir

        #Get GRAM and LCD width and height
        if (Scan_dir == config.L2R_U2D) or (Scan_dir == config.L2R_D2U) or (Scan_dir == config.R2L_U2D) or (Scan_dir == config.R2L_D2U) :
            self.width	= config.LCD_HEIGHT 
            self.height = config.LCD_WIDTH 
            if Scan_dir == config.L2R_U2D:
               MemoryAccessReg_Data = 0X00 | 0x00
            elif Scan_dir == config.L2R_D2U:
               MemoryAccessReg_Data = 0X00 | 0x80
            elif Scan_dir == config.R2L_U2D:
               MemoryAccessReg_Data = 0x40 | 0x00
            else:		#R2L_D2U:
                MemoryAccessReg_Data = 0x40 | 0x80
        else:
            self.width	= config.LCD_WIDTH 
            self.height = config.LCD_HEIGHT 
            if Scan_dir == config.U2D_L2R:
                MemoryAccessReg_Data = 0X00 | 0x00 | 0x20
            elif Scan_dir == config.U2D_R2L:
                MemoryAccessReg_Data = 0X00 | 0x40 | 0x20
            elif Scan_dir == config.D2U_L2R:
                MemoryAccessReg_Data = 0x80 | 0x00 | 0x20
            else:		#R2L_D2U
                MemoryAccessReg_Data = 0x40 | 0x80 | 0x20

        #please set (MemoryAccessReg_Data & 0x10) != 1
        if (MemoryAccessReg_Data & 0x10) != 1:
            self.LCD_X_Adjust = config.LCD_Y
            self.LCD_Y_Adjust = config.LCD_X
        else:
            self.LCD_X_Adjust = config.LCD_X
            self.LCD_Y_Adjust = config.LCD_Y

        # Set the read / write scan direction of the frame memory
        self.command(ST7735.MADCTL)		#MX, MY, RGB mode 
        self.data( MemoryAccessReg_Data | 0x08)	#0x08 set RGB

    def Init(self):
        self.module_init()
        self.reset()

        #65k mode
        self.command(ST7735.COLMOD)
        self.data(0x05) #16 bit color.

        #ST7735R Frame Rate
        #Frame rate control.
        self.command(ST7735.FRMCTR1)
        #fastest refresh, 6 lines front, 3 lines back.
        self.data(ST7735.SWRESET)
        self.data(ST7735.RAMWR)
        self.data(0x2D)

        #Frame rate control.
        self.command(ST7735.FRMCTR2) 
        #fastest refresh, 6 lines front, 3 lines back.
        self.data(ST7735.SWRESET)
        self.data(ST7735.RAMWR)
        self.data(0x2D)

        #Frame rate control.
        self.command(ST7735.FRMCTR3) 
        #fastest refresh, 6 lines front, 3 lines back.
        self.data(ST7735.SWRESET)
        self.data(ST7735.RAMWR)
        self.data(0x2D)
        self.data(ST7735.SWRESET)
        self.data(ST7735.RAMWR)
        self.data(0x2D)

        # Display inversion control
        self.command(ST7735.INVCTR)
        self.data(0x07) #Line inversion.

        #ST7735R Power Sequence
        self.command(ST7735.PWCTR1)
        self.data(0xA2) 
        self.data(0x02)
        self.data(0x84)

        self.command(ST7735.PWCTR2)
        self.data(0xC5) #VGH = 14.7V, VGL = -7.35V

        self.command(ST7735.PWCTR3)
        self.data(0x0A) #Opamp current small
        self.data(0x00) #Boost frequency

        self.command(ST7735.PWCTR4)
        self.data(0x8A) #Opamp current small
        self.data(0x2A) #Boost frequency

        self.command(ST7735.PWCTR5)
        self.data(0x8A) #Opamp current small
        self.data(0xEE) #Boost frequency

        self.command(ST7735.VMCTR1) #VCOM 
        self.data(0x0E)

        #ST7735R Gamma Sequence
        self.command(ST7735.GMCTRP1)
        self.data(0x0f)
        self.data(0x1a)
        self.data(0x0f)
        self.data(0x18)
        self.data(0x2f)
        self.data(0x28)
        self.data(0x20)
        self.data(0x22)
        self.data(0x1f)
        self.data(0x1b)
        self.data(0x23)
        self.data(0x37)
        self.data(0x00)
        self.data(0x07)
        self.data(0x02)
        self.data(0x10)

        self.command(ST7735.GMCTRN1)
        self.data(0x0f)
        self.data(0x1b)
        self.data(0x0f)
        self.data(0x17)
        self.data(0x33)
        self.data(0x2c)
        self.data(0x29)
        self.data(0x2e)
        self.data(0x30)
        self.data(0x30)
        self.data(0x39)
        self.data(0x3f)
        self.data(0x00)
        self.data(0x07)
        self.data(0x03)
        self.data(0x10)

	    #Enable test command
        #self.command(0xF0)
        #self.data(ST7735.SWRESET)

        #Disable ram power save mode
        #self.command(0xF6)
        #self.data(0x00)

        self.SetGramScanWay(config.SCAN_DIR_DFT)

        #self.command(0x11)

        self.command(ST7735.DISPON)


    def SetWindows(self, Xstart, Ystart, Xend, Yend):
        #set the X coordinates
        self.command(ST7735.CASET)
        self.data(0x00)               #Set the horizontal starting point to the high octet
        self.data((Xstart & 0xff) + self.LCD_X_Adjust)      #Set the horizontal starting point to the low octet
        self.data(0x00)               #Set the horizontal end to the high octet
        self.data(((Xend - 1) & 0xff) + self.LCD_X_Adjust) #Set the horizontal end to the low octet 
        
        #set the Y coordinates
        self.command(ST7735.RASET)
        self.data(0x00)
        self.data((Ystart & 0xff)  + self.LCD_Y_Adjust)
        self.data(0x00)
        self.data(((Yend - 1) & 0xff ) + self.LCD_Y_Adjust)

        self.command(ST7735.RAMWR) 
        
    def ShowImage(self,Image):
        """Set buffer to value of Python Imaging Library image."""
        """Write display buffer to physical display"""

        # holy fucking shit.
        imwidth, imheight = Image.size
        if imwidth != self.width or imheight != self.height:
            raise ValueError('Image must be same dimensions as display \
                ({0}x{1}).' .format(self.width, self.height))
        img = self.np.asarray(Image)
        pix = self.np.zeros((self.width,self.height,2), dtype = self.np.uint8)
        pix[...,[0]] = self.np.add(self.np.bitwise_and(img[...,[0]],0xF8),self.np.right_shift(img[...,[1]],5))
        pix[...,[1]] = self.np.add(self.np.bitwise_and(self.np.left_shift(img[...,[1]],3),0xE0),self.np.right_shift(img[...,[2]],3))
        pix = pix.flatten().tolist()
        self.SetWindows ( 0, 0, self.width, self.height)
        self.digital_write(self.GPIO_DC_PIN,True)
        for i in range(0,len(pix),4096):
            self.spi_writebyte(pix[i:i+4096])		
        
    def clear(self):
        """Clear contents of image buffer"""
        _buffer = [0xff]*(self.width * self.height * 2)
        self.SetWindows ( 0, 0, self.width, self.height)
        self.digital_write(self.GPIO_DC_PIN,True)
        for i in range(0,len(_buffer),4096):
            self.spi_writebyte(_buffer[i:i+4096])	        
        

