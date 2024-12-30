
import time
import core.disp_drivers.ST7735.config as config

class ST7735(config.RaspberryPi):

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
        self.command(0x36)		#MX, MY, RGB mode 
        self.data( MemoryAccessReg_Data | 0x08)	#0x08 set RGB

    def Init(self):
        self.module_init()
        self.reset()

        #ST7735R Frame Rate
        self.command(0xB1)
        self.data(0x01)
        self.data(0x2C)
        self.data(0x2D)

        self.command(0xB2)
        self.data(0x01)
        self.data(0x2C)
        self.data(0x2D)

        self.command(0xB3)
        self.data(0x01)
        self.data(0x2C)
        self.data(0x2D)
        self.data(0x01)
        self.data(0x2C)
        self.data(0x2D)

        #Column inversion 
        self.command(0xB4)
        self.data(0x07)

        #ST7735R Power Sequence
        self.command(0xC0)
        self.data(0xA2)
        self.data(0x02)
        self.data(0x84)
        self.command(0xC1)
        self.data(0xC5)

        self.command(0xC2)
        self.data(0x0A)
        self.data(0x00)

        self.command(0xC3)
        self.data(0x8A)
        self.data(0x2A)
        self.command(0xC4)
        self.data(0x8A)
        self.data(0xEE)

        self.command(0xC5) #VCOM 
        self.data(0x0E)

        #ST7735R Gamma Sequence
        self.command(0xe0)
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

        self.command(0xe1)
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
        self.command(0xF0)
        self.data(0x01)

        #Disable ram power save mode
        self.command(0xF6)
        self.data(0x00)

        #65k mode
        self.command(0x3A)
        self.data(0x05)

        self.SetGramScanWay(config.SCAN_DIR_DFT)

        self.command(0x11)

        self.command(0x29)


    def SetWindows(self, Xstart, Ystart, Xend, Yend):
        #set the X coordinates
        self.command(0x2A)
        self.data(0x00)               #Set the horizontal starting point to the high octet
        self.data((Xstart & 0xff) + self.LCD_X_Adjust)      #Set the horizontal starting point to the low octet
        self.data(0x00)               #Set the horizontal end to the high octet
        self.data(((Xend - 1) & 0xff) + self.LCD_X_Adjust) #Set the horizontal end to the low octet 
        
        #set the Y coordinates
        self.command(0x2B)
        self.data(0x00)
        self.data((Ystart & 0xff)  + self.LCD_Y_Adjust)
        self.data(0x00)
        self.data(((Yend - 1) & 0xff ) + self.LCD_Y_Adjust)

        self.command(0x2C) 
        
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
        

