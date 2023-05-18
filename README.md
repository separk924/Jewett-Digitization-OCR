# training-jewett

## Description

This project attempts to transcribe Stanley Jewett's cursive handwritten diaries using Tesseract's optical character recognition (OCR) engine. The main stages of the project pipeline were pre-processing, training, post-processing, and testing of the model. Python's OpenCV and NumPy packages were used for pre-processing. Training was compounded on top of a pre-trained Tesseract OCR Engine, and the post-processing stage involved using a custom dictionary and the SpaCy natural language processing model to correct inaccuracies. The model was tested by making predictions on new images and comparing the output to human-transcribed text. After completing some sample tests, the character error rate (CER) was approximately 18\% without post-processing. After, it achieved a 3\% CER on one line, but the average edit distance was 11.6 characters. Future work involves expanding the data-set, improving pre-processing for complex pages, exploring alternative OCR methods, and enabling public access to Stanley Jewett's notes.

<p align="center">
   <img src="/our_files/img043copy.jpg"  width="200" height="300">
</p>

This project pipeline consisted of multiple steps in the training and testing process. We take scans of pages from a journal, and then pre-process the images. First, we convert to grayscale, then binarize the image, and lastly remove any dotted lines from the image. Next, we create the files needed to train Tesseract 5 by splitting the page images into individual lined tiff files, box files, and ground truth text files. The next part of the training pipeline is to train Tesseract on Jewett’s handwriting with this data-set. We then use the trained model to recognize the text on the pre-processed testing images and then run it through post-processing which attempts to correct words that are misspelled.

<p align="center">
   <img src="/our_files/project_pipeline.png"  width="450" height="250">
</p>

**Tesseract's Basic Architecture:**

<p align="center">
   <img src="/our_files/tesseract.png"  width="450" height="250">
</p>

To further train Tesseract on Stanley Jewett’s handwriting, Jewett’s handwriting was treated as another font. Three files per datum were required to run the training: a Tiff file, a Box file, and a Ground Truth text file. A Tiff file is the actual lines image, a box file contains the coordinates, widths, heights, and character mappings of each letter on the line. In total, 348 line images were manually created, and after training on varying amounts of epochs the best accuracy on training and testing we achieved was 3,000 epochs. 

## Pre-Processing

All images were pre-processed using the Python packages, OpenCV (Open Source Computer Vision Library) and NumPy. Initially, we start with a high quality scan of a page that is then converted to gray scale. The next stage is the most important, and it is known as image binarization or thresholding. In order to remove unwanted lines, we used OpenCV’s connected components function to find all connected components on an image, and filter out pixels less than a certain size. This allowed us to remove these lines without significant alterations to the text. Messier notebooks followed this same four-stage process, but with one added noise removal step. To perform this extra step, Gaussian Blur was applied to the entire image with a kernel size of 3.

<p align="center">
   <img src="/our_files/preprocessing_ex.png"  width="360" height="430">
</p>

## Prepare for Training

These links were referenced to run Training on Tesseract 5:

[Gabriel Garcia's Tutorial Github Repo](https://github.com/astutejoe/tesseract_tutorial)

[Gabriel Garcia's Tutorial Youtube Video](https://www.youtube.com/watch?v=KE4xEzFGSU8)

[The Code's Tutorial Youtube Video](https://www.youtube.com/watch?v=1v8BPw0Dn0I)

This is the link that provides the download for JTessBoxEditor:

https://sourceforge.net/projects/vietocr/files/jTessBoxEditor/

Make sure to download the latest version that does not have FX in the file name. In addition to this, make sure to have the latest Java JDK version updated on your computer before downloading JTessBoxEditor.

1. Download Tesseract 5 using the command line:
   ```
   brew install tesserac
   ```
2. Download JTessBoxEditor

** Keep all 3 files in the same directory and name this directory: /jewett-ground-truth

3. Create Tiff files:

   a. Create single-line images (jpg or png is fine)
   
   b. Go into the JTessBoxEditor directory in the terminal, and open JTessBoxEditor by running this command line:
      ```
      java -Xms128m -Xmx1024m -jar jTessBoxEditor.jar
      ```
      
   c. Click on Tools tab, and then click on Merge Tiff option to create tiff files one-by-one for each line image file
   
4. Create Ground Truth files:

   a. provide transcription for each line image. This should contain just 1 line of text transcribing the words in the line image
   
5. Create Box files:

   a. Go into the directory with the tiff files and ground truth files in the terminal and run this line:
   
      ```
      tesseract [langname].[fontname].[expN].[file-extension] [langname].[fontname].[expN] batch.nochop makebox
      Eg:tesseract jewett.eng.exp0.tif jewett.eng.exp0 batch.nochop makebox
      ```
      
      This should create all of the box files that contain the coordinates and sizes of each character in the file. It will also provide the guesses for each character. You must go through them one-by-one and correct the coordinates, sizes, and guesses.

## Run Training

1. In the tesstrain directory, create a /data directory and move the /jewett-ground-truth directory into the /data directory

2. Replace the Makefile in the tesstrain directory with the one provided in the /our_files directory

3. On the command line, run this line in the /tesstrain directory to begin training:

   ```
   TESSDATA_PREFIX=../tesseract/tessdata make training MODEL_NAME=jewett START_MODEL=eng TESSDATA=../tesseract/tessdata MAX_ITERATIONS=3000
   ```
   
   a. The current /tessdata directory may not work. If so, use the tessdata_best Github repo instead. Delete the /tessdata directory that's inside the /tesseract directory, and clone this directory inside of the /tesseract directory:
   
      ```
      git clone https://github.com/tesseract-ocr/tessdata_best.git
      ```
      
   b. Then rename the /tessdata_best directory to /tessdata, and try to rerun the command line for training
   
   c. The created files and its structure should look like this:
      <p align="center">
         <img src="/our_files/created_files_structure.png"  width="200" height="500">
      </p>
   d. LSTMF files should also appear in the /jewett-ground-truth directory:
      <p align="center">
         <img src="/our_files/jtg-lstmf.png"  width="200" height="470">
      </p>
      
4. The created model should appear in the tesstrain/data/ directory. It will appear as `jewett.traineddata`.

## Post-Processing

## Run Model

## Output

## Future Work

## Credits
