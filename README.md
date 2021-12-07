# Scheduler50
Description:
This locally hosted website allows users to schedule events with other users and select the best time to host an event (an improved when2meet if you will).

Languages Used:
HTML, CSS, JavaScript, Jinja (with Flask), SQL, Python

Challenges and plans for the future:
We struggled a lot initially with collaborating via git with merge conflicts causing quite a lot of problems. The other largest problem was with time zone conversion as we had an intuitive idea of how we thought it could work, but we turned out to be vastly wrong. We also planned to have google calendar integration but after struggling for more than two days with it and having got nowhere we decided to rather focus on the other parts of the project.

How to use the project:
When you open the project you are taken to the login screen where you can log in if you have already registered or 
Register yourself as a user and send the link (should it be published) to your friends/colleagues to register themselves (register.html).

After that, you will be directed to the home screen (index.html) where you will see all of the future events you have ahead of you. This can be filtered to show past events. With each event, you can edit the event's details through the edit button (which will take you to create.html with some buttons unhidden). You can also view the responses to the event and what times work for everyone (if you click on the responses button which takes you to repsonses.html). If you click on the event title you will see in red the times that you cannot make (filled out through the preferences side) and you can select the times (which will turn green that you can make it). This is what we have called selecttimes.html because it allows the user to select their available times.

You can also access via the navigation bar create, preferences, contacts and should you click on Scheduler50 you will be taken back to this home page. If you click on create you will be asked to fill in the details of your event (create.html) and on clicking next you will be allowed to invite users to your event (addinvitees.html). After clicking next you will be taken to selecttimes.html where you can select the times that you are available and then after submitting the form you will be taken back to the home page.

If you click on Preferences on the navigation bar (preferences.html) you will be taken to a generic week where you can block out times that you can't ever make. If you click on Contacts on the navigation bar (contacts.html) you will see an unordered list of those who you have invited to previous events. Lastly, if you click logout, the program "forgets" the user id and takes you back to the login page.

Should there be a user error or other HTML error the apology.html page will run and display a photo of a cat with the error code and its description. 

Alternative uses to the project:
You could consider building on this project and adding additional functionality or publishing this website.
You could use it to see the interaction between the different programming languages used to give yourself a practical example of how to use it.

Credits:
Matthew Andrews
https://github.com/MHAndrews
Grayson Martin
https://github.com/GraysonMMartin 

How to contribute:
Clone this repository and work on anything you are interested in. Then either email matthew_andrews@college.harvard.edu or graysonmartin@college.harvard.edu and we can talk about adding you as a collaborator. 

License:
Can be viewed at License.md