if __name__ == '__main__':
    import os
    import argparse
    from PIL import Image

    """This Function Handles all the logic of formatting the image"""
    # TODO: Reformat to handle output by return variable instead of manually returning output + exit
    def format_output(image, file_format: str, old_file_size: int, compression_method) -> None:
        # Only allow supported file formats,
        # see https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
        match file_format:
            case "JPEG":
                file_extension = ".jpg"
                file_format = "JPEG"
            case "PNG":
                file_extension = ".png"
                file_format = "PNG"
            case _:
                print(f"Invalid file format supplied! {file_format} was supplied to format_output!")
                exit(101)

        outfile = f"{file}_compressed{file_extension}"
        formatted_output = f"{img_output_loc}/{outfile}"

        global RedundantCount
        global ImgQuality

        # If User does not want to convert small images, do not keep them.
        if SmallImgFlag == 2:
            if image.size[0] <= SmallImgSize or image.size[1] <= SmallImgSize:
                RedundantCount += 1
                return None

        # Set maximum size to requested MaxSize flag if applicable
        if args.MaxSize is None:
            size = image.size
        else:
            size = (args.MaxSize, args.MaxSize)

        # Prompt User to change size if we surpass requested PromptSize flag
        if args.PromptSize is not None:
            if image.size[0] > args.PromptSize or image.size[1] > args.PromptSize:
                answer = input(f"Do you wish to limit the size of {infile} to {args.PromptSize}? [y/n] ")
                if answer.lower() in ["y", "yes"]:
                    size = (args.PromptSize, args.PromptSize)
                    print(f"Resizing has been applied!")
                elif answer.lower() in ["n", "no"]:
                    size = image.size
                else:
                    print(f"Invalid Input!")
                    size = image.size

        image.thumbnail(size, compression_method)
        image.save(formatted_output, format=file_format, optimize=True, quality=ImgQuality)

        # If the filesize is bigger than before, then there is no point in keeping the result
        compressed_file_size = int(os.path.getsize(formatted_output))
        if compressed_file_size > old_file_size:
            os.remove(formatted_output)
            RedundantCount += 1


    def clamp(num: int, min_num: int, max_num: int) -> int:
        return max(min(max_num, num), min_num)


    # Flags
    parser = argparse.ArgumentParser()

    # -PromptSize PromptSize -MaxSize MaxSize -ConvertSmallImg ConvertSmallImg
    # -SmallImgSize SmallImgSize -ImgQuality ImgQuality
    parser.add_argument("-PromptSize", "--PromptSize", help="Photo Length or Height to prompt for adjustment", type=int)
    parser.add_argument("-MaxSize", "--MaxSize", help="Maximum Photo Length or Height that any Photo can have",
                        type=int)
    parser.add_argument("-ConvertSmallImg", "--ConvertSmallImg",
                        help="Convert Small Images that might not give minor to no improvements. Defaults to no. "
                             "Valid Cases: yes/no/warn", type=str)
    parser.add_argument("-SmallImgSize", "--SmallImgSize", help="Height or Width of an image to be considered a small "
                                                                "image", type=int)
    parser.add_argument("-ImgQuality", "--ImgQuality", help="Percentage of Quality to remain in final image. "
                                                            "Valid values are 0-100. Defaults to 90", type=int)
    parser.add_argument("-CompressionMethod", "--CompressionMethod",
                        help="Choose what Compression Method will be used on images. Defaults to LANCZOS. "
                             "EXPERIMENTAL! PROBABLY BUGGY!", type=str)

    args = parser.parse_args()

    # Process all possible Flags

    # Clamp Size Flags to prevent crashes
    if args.PromptSize is not None:
        clamp(args.PromptSize, 1, 2_000_000)

    if args.MaxSize is not None:
        clamp(args.MaxSize, 1, 2_000_000)

    if args.SmallImgSize is None:
        SmallImgSize = 512

    if args.ImgQuality is not None:
        clamp(args.ImgQuality, 1, 100)
    else:
        ImgQuality = 90

    # ConvertSmallImg Flag, 0 = Invalid, 1 = Yes, 2 = No
    match args.ConvertSmallImg:
        case "yes":
            SmallImgFlag = 1
        case "no" | None:
            SmallImgFlag = 2
        case _:
            SmallImgFlag = 0
            print(f"Invalid ConvertSmallImg flag given! {args.ConvertSmallImg} is not valid!")
            exit(104)

    # CompressionMethod Flag, 0 = Invalid, Regularly typed methods for compression methods.
    match args.CompressionMethod:
        case "Lanczos" | None:
            CompressionMethodFlag = Image.LANCZOS
        case "Nearest":
            CompressionMethodFlag = Image.NEAREST
        case "Box":
            CompressionMethodFlag = Image.BOX
        case "Bilinear":
            CompressionMethodFlag = Image.BILINEAR
        case "Hamming":
            CompressionMethodFlag = Image.HAMMING
        case "Bicubic":
            CompressionMethodFlag = Image.BICUBIC
        case _:
            CompressionMethodFlag = 0
            print(f"Invalid CompressionMethod flag given! {args.CompressionMethod} is not valid!")
            exit(105)

    # Image Related Variables
    img_loc = "img"
    img_output_loc = "img_compressed"

    # Statistics Related Variables
    SuccessCount = 0
    FailureCount = 0
    RedundantCount = 0

    # Check if image folder is set up
    if not os.path.exists(img_loc):
        try:
            os.mkdir(img_loc)
        except OSError:
            print(f"Creation of the directory {img_loc} failed, this program needs write access!")
        else:
            print(f"The Image folder does not exist! Please add your images in the new img folder!")
        exit(102)

    if not os.listdir(img_loc):
        print(f"There are no images in {img_loc}! Please add images to compress!")
        exit(103)

    print(os.listdir(img_loc))

    try:
        os.mkdir(img_output_loc)
    except OSError:
        print(f"The {img_output_loc} folder already exists. Skipping creation")
    else:
        print(f"Successfully created the directory {img_output_loc}")

    for infile in os.listdir(img_loc):
        file, extension = os.path.splitext(infile)
        img_path = f"{img_loc}/{infile}"
        try:
            uncompressed_file_size = int(os.path.getsize(img_path))
            with Image.open(img_path) as im:
                # print(im.format, im.size, im.mode)
                format_output(im, im.format, uncompressed_file_size, CompressionMethodFlag)
                SuccessCount += 1
        except OSError:
            print(f"cannot convert {infile}")
            FailureCount += 1

    print(f"Successfully converted {SuccessCount} images! "
          f"Failed to convert {FailureCount} images! "
          f"{RedundantCount} images were deemed redundant due to settings or increased file size")
