# ImageCompressor
 Small Batch Image Compressor made for personal use, mostly meant to compress uncompressed files where it makes sense to do so.
 This Script will not save images if the compressed version becomes larger in size than the original version, which is a common issue when compressing already compressed files.

 This Python Script uses PILLOW to compress images through the usage of different flags.

 ## (Optional) Flags
  * ### -PromptSize 
    > Photo Length or Height to prompt for adjustment.  
    Valid values are 1 to 2.000.000

  * ### -MaxSize 
    > Maximum Photo Length or Height that any Photo can have.  
    Valid values are 1 to 2.000.000

  * ### -ConvertSmallImg
    > Convert Small Images that might not give minor to no improvements.  
    Defaults to no  
    Valid Cases: yes/no/warn

  * ### -SmallImgSize 
    > Height or Width of an image to be considered a small image.  
    Valid values are 1 to 2.000.000  
    Defaults to 512

  * ### -ImgQuality 
    > Percentage of Quality to remain in final image.  
    Valid values are 0-100  
    Defaults to 90.

  * ### -CompressionMethod 
    > Choose what Compression Method will be used on images. Defaults to LANCZOS.  
    Valid options are: LANCZOS, NEAREST, BOX, BILINEAR, HAMMING and BICUBIC.  
    This flag is experimental and most likely will produce some bugs or unwanted results!

 ## Instructions
  You can use this Script with the following steps:
  1. Place your uncompressed images in the "img" folder.
  2. Run Main.py with any additional flags
  3. Wait for the images to compress.
  4. Check the end result in the "img_compressed" folder!
