# Movies-Prototype
 
Original Source codes: contains original source codes, in case we need it we can find it here

Pages: Contains both front end and admin pages



!IMPORTANT! 
code to know which task, "letter" + "number"
remember to check the item you finished
when commiting, if you finished a certain task say, finished tasks: e.g. H1, P1

## Front End
* H - home page
    1. decide if new items under carousel is needed 
        - if so what is the content? e.g differentiate book/rent movies
    2. decide what to put under catalog list  √
    3. finish carousel √
    * New Carousel concept to suit our new webpage: if carousel can only hold n number of  items we do another concept which is if we keep adding new items it only shows the n latest carousel entry √
    4. decide what to do for "show more"  X
    5. Ensure login works for users √
    6. add related images such as logo etc. √
    7. make content in carousel page clickable. 

* P - promotion page
    1. promotion page revamp: design √

* B - booking movie page
    1. Booking movies page revamp: UI will need to suit our needs 
    
* C - movielist/catalog page
    1. nav name is "CATALOG"  
    2. UI will need to change
    3. When you click on play for movie, a modal with the video trailer will appear
    4. Ensure it retrieves from shelve

* M - movie page 
    1. Movie detail page is dynamic √
    2. Has rent an/or book movie button X

* R - rent movie page
    1. Rent movie page need revamp 

* T - theatre page
    1. additional attribute, theatre location (KIV)
    
* G - general
    1. Fix routing of new webpages √
    2. Add flash inside user2.html  √ Partially
    3. sign up page form field inconsistent****** √
    4. When running: ensure admin account is created, genre list is also created √
    5. Have related images downloaded and implemented X
    6. pages such as about page,privacy policy etc to be done or removed.  √
    7. Handling errors √
    8. Legal page (Terms and conditons to be put at the checkouts of any online purchases******) √
    9. About Us page     √


                                
## Admin
* A - admin
    1. Change design of Admin pages: showing of details looks weird and not appealing  
    2. Modify dash board to suit our needs 
    3. Login for admin staff √
    4. Create a page to manage multiple admin √
    5. When choosing genre for a movie, you can choose multiple genres link √
    6. When initializing a movie, rating is nil and people can change its value by up voting or otherwise (50%) X
    7. When choosing timeslot, multiple options √  
    8. Generate Pdf
    9. Change IDs to have letter.  √
    10. Carousel revamp. getting information from  promotion and movies dictionary to be parse into the carousel dictionary.******* √
    11. All forms require proper validation
        * Rental: cannot upload duplicate rental 
    12. modify movie > routes.py > genre list missing √
    13. modify function for pages doesnt have validation when certain features are not selected 
    14. Modify movie image source error X
    15. Deleting Movie doesn't work X
    
    
## Useful Links
* Multiselect link -> https://www.cssscript.com/multi-select-dropdown-component-javascript-slim-select/

## Priorities
* High
    1. create on hold seat attribute √
    2. check if seat is on hold √
    3. image of movie in showtime √
    4. when click on movie image will show trailer in modal √
    5. Form validation for all admin pages √
    6. Form validation for sign up form √
    7. must remember what the users had selected and allow them to change
    8. seats must be independent from each other
    9. seats dict should have their own key √ 
    10. on admin side can see who booked the seats at the moment
    11. if no theatre, movie added, must tell user that you cannot add showtime

* Medium
    1. checkout with stripe
    2. timer for check out - showtime
    3. login user log them out if they idle too long
    4. make content in carousel page clickable. 
    5. Generate pdf for check out  
    6. ModifyShowtime in routes.py flash message √

allo help me with smthing ??????
add in the filter thing for movies (catalog)
and also come voice call wait the filter i delete the year and rating 
can be fking crazy and allow user to update the ratings oof
* Low
