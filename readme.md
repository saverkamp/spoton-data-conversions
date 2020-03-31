## Spot On Data Conversion Scripts

Scripts for porting your personal data from Planned Parenthood's [Spot On](https://www.plannedparenthood.org/get-care/spot-on-period-tracker) period tracking app to  two alternatives, [Drip](https://bloodyhealth.gitlab.io/) and [Clue](https://helloclue.com/). 

Until January of 2020, Planned Parenthood offered a simple but effective period tracking app. While less fully-featured than its competitors, Spot On did a few things really well, such as easy-to-manage birth control and period reminders and customizable calendar visualizations making it easy to see variations in flow, pain, mood, or any other data points collected. The best feature, in my opinion, was the ability to create custom properties for anything not already covered by the app. There are many reasons people use period tracking apps besides preventing or achieving pregnancy, so this simple and flexibile feature enabled the app to support a wide range of use cases without having to design for each one. (You can see the old app design at the [designer's website](http://isarchang.com/project/spot-on-period-tracker) and the [Internet Archive](https://web.archive.org/web/20191103205736/https://www.plannedparenthood.org/get-care/spot-on-period-tracker).)

At the end of January, without warning, Planned Parenthood pushed a complete redesign of the app to users' phones, deleting some users' data, locking some users out, and showing users inaccurate information about their cycles and birth control schedules. You can read reviews at the [Google Play Store](https://play.google.com/store/apps/details?id=com.spotontracker&hl=en_US) and the [App Store](https://apps.apple.com/us/app/spot-on-period-tracker/id1039914781) as well as [this blog post](https://researcheraccidentally.com/2020/01/31/periodtrackerapppt1/) for the full rundown of everything that's now wrong with this app, but in a nutshell, the three great features above are now changed or gone (custom emojis suddenly disappeared one day in early March), making this app basically useless for my purposes. You can also no longer export your data from the app (or at least not on Android), so hopefully you opted in to automatic backups at some point before the redesign. I wrote to the Spot On team over a month ago to see about getting a data export, but like many reviewers, I have not received a reply.  

I really don't like having to write this about Planned Parenthood because I support their mission and efforts at just about everything else they do, but I feel sick and betrayed by their mishandling of my personal data and lack of communication with their users. Tracking and managing data about your own body is just one of many acts of empowerment that I know Plannned Parenthood supports, so I expected more care and sensitivity from them when rolling out such major changes. I hope they can eventually get their app reverted or functioning again (or give up on the period tracking business and redirect that funding line to something more vitally important), but in the meantime, I hope they can do the responsible thing and give users their own data back.  

After some digging around in my Google Drive for any backups I might have kept, I found a "Spot On Info.spa" file which turned out to be a zip archive containing all of my data auto-updated to the date of the redesign. I had already started using Drip and Clue, but I was able to successfully convert my Spot On data and merge it with data I'd already entered into each app. There are many period trackers out there to choose from, each with different strengths and weaknesses with regards to features and [data](https://chupadados.codingrights.org/en/menstruapps-como-transformar-sua-menstruacao-em-dinheiro-para-os-outros/) [privacy](https://www.privacyinternational.org/long-read/3196/no-bodys-business-mine-how-menstruations-apps-are-sharing-your-data). I chose Drip because it's one of the only (or the only?) open-source period tracking projects under active development, and I think it's important to support open and transparent processes around managing our personal health data. Drip is still in beta (and not yet available on iOS), and it doesn't yet manage any data related to hormonal birth control, but it does enable tag creation similar to Spot On's custom emoji. Drip does not yet have a data privacy policy, but their homepage says "Everything stays on your device." Clue has been around a bit longer than Drip and tracks hormonal birth control in addition to many other health and activity facets. It also allows for custom tags, like Drip and Spot On. Clue is a German company, which means it has to comply with the [GDPR](https://en.wikipedia.org/wiki/General_Data_Protection_Regulation) and basically be more careful with your data. Requirements aside, their [data privacy policy](https://helloclue.com/privacy) is incredibly clear and a model for what all data privacy policies should look like. Clue does not share your data with third parties, but it will share your de-identified data with "carefully-selected" health researchers, according to their privacy policy and [blog](https://helloclue.com/articles/about-clue/the-journey-of-a-single-data-point).  

### Let's get started
*DISCLAIMER: I use an Android phone (Pixel 2) and have only had access to my own data in writing these scripts. Your mileage may vary with iOS or your own data. (Pull requests and feedback are welcome if you run into issues.) Make sure you always work from copies of your data! These scripts will not alter your existing Spot On data or Drip or Clue exports, but they do require you move some files around, so better to be safe.*  
  
*ALSO, these scripts require that you install Python 3 and can run simple commands in a terminal or a command line interface. If this seems out of reach for you, please feel free to get in touch, and I can try to do the conversions for you.*  

Once you find your data, this is a two-script process. The first script will read in your Spot On data and create a customized mapping from Spot On datafields to either Drip or Clue. You'll open this mapping in a spreadsheet editor (Google Sheets, Microsoft Excel, Numbers, etc.) and edit it so that your custom emoji will map to the data fields of your choosing in Drip or Clue. You'll save this edited mapping as a CSV file for the next script, which will read in your mapping and your Spot On data and output a data file to import into your target app.  

1. Find your data
2. Create your custom mapping  
3. Edit your mapping  
4. Create your new data import  

### Find your data
If you think you might have set up automatic backups at some point, search in your Google Drive or iCloud account for "Spot On Info.spa". If you find this file, download a copy to your computer. (It's possible the backup exists somewhere on your phone, but I wasn't able to find one on mine.)  

Next, download this GitHub code to your computer by clicking the green "Clone or Download" button above and selecting "Download ZIP". Unzip this folder somewhere on your computer and move the copy of "Spot On Info.spa" into the unzipped folder.  

### Create your custom mapping
Open a terminal or command line window in the GitHub folder you just unzipped. (On MacOS you can right-click and select "New Terminal at Folder". On Windows, hold shift and right-click then select "Open command window here")  

To create a mapping to Drip, type the following command (for all commands, use the Python command appropriate to your installation: "python" or "python3"):  

`python3 Drip`  

To create a mapping to Clue, type the following command:  

`python3 Clue`  

First the script will unzip your "Spot On Info.spa" file and create a new folder called "spoton_data" in your GitHub folder. (Don't move or change anything in this folder.) Next the script should create a "my_spoton-to-drip_mapping.csv" or "my_spoton-to-clue_mapping.csv" file, depending on your destination app.  You'll edit this mapping to include your custom emoji.  

### Edit your mapping (Drip)  
Open your "my_spoton-to-drip_mapping.csv" file in a spreadsheet editor like Google Docs, Microsoft Excel or Numbers. You should see a list of all your Spot On data fields in column A and the Drip fields in column B. Towards the bottom of column A, you'll see all of the custom emoji you created in the app (these start with "E-"). You'll notice that these fields do not have mappings in the "Drip_field" and "Drip_value" columns. For each of these you have number of options for mapping:
1. **Map the Spot On field to one of the non-note Drip fields above.** Move the field to a blank space if the semantics match up for you. For instance, I had created a custom emoji called "E-Back pain". This matches up with "pain.backache" in Drip, so I moved "E-Back pain" to the empty Spot On cell in that row. If you have more than one Spot On field that would map to a Drip field, you can just copy and paste the Drip_field and Drip_value into the empty cells next to the Spot On fields.
2. **Map the Spot On field to a note field.** Drip has general notes ("note.value") and notes specific to some of the categories (ex. "mood.note"). To map a Spot On field to a Drip note field, follow the instructions above but replace "text" in the "Drip_value" column to the text you would to show up in the Drip note field. For example, for the Spot On field "E-Drank alcohol", I entered the note "note.value" in the "Drip_field" cell and "alcohol" in the "Drip_value" cell so that this custom emoji will appear in drip as a general note. 
3. If you don't want the data from a Spot On field to show up in your Drip data, you can simply **delete it.** 

There are some Spot on fields I included in the default mapping that you might want to adjust to your preferences:
- "MoodFrisky" defaults to "desire.value" with a value of "2-high". You can change this your liking by moving the Spot On field to the desired level. (Do not adjust the Drip fields or values.)
- "ActionHadSex" defaults to "sex.partner" in Drip. You'll see there are a lot of other options, "sex.solo" and many variations on protected sex. You can move "ActionHadSex" to any of these, if you prefer. If you move it to "sex.note" you should replace "note" in "Drip_value to whatever note you would like to appear in Drip. (You can also go in and change individual instances of these in the app after you've imported the data.)  

Once you've finished make sure that every Spot On field with a value also has values next to it in the "Drip_field" and "Drip_value" columns. Now export your spreadsheet as a CSV file and name it the same as the CSV you imported, "my_spoton-to-drip_mapping.csv". When you're finished, it should look something like [this](https://github.com/saverkamp/spoton-data-conversions/blob/master/sample_edited_spoton-to-drip_mapping.csv). Save this file to your GitHub folder.  

### Edit your mapping (Clue)
Open your "my_spoton-to-clue_mapping.csv" file in a spreadsheet editor like Google Docs, Microsoft Excel or Numbers. You should see a list of all your Spot On data fields in column A and the Clue fields in columns B-D. Towards the bottom of column A, you'll see all of the custom emoji you created in the app (these start with "E-"). You'll see that these fields do not have mappings in the "Clue_field", "Clue_datatype" and "Clue_value" columns. For each of these you have number of options for mapping:
1. Map the Spot On field to one of the Clue fields above. Move the field to a blank space if the semantics match up for you. For instance, I had created a custom emoji called "E-Drank alcohol". This matches up closely enough with "party"/"drinks_party" in the "Clue_field"/"Clue_value", so I moved "E-Drank alcohol" to the empty Spot On cell in that row. If you have more than one Spot On field that would map to a Clue field, you can just copy and paste the cells from "Clue_field", "Clue_datatype" and "Drip_value" into the empty cells next to the Spot On fields.
2. For any Spot On fields that don't map to Clue fields, you can show them as tags in the Clue app. enter "tags" in the "Clue_field" cell, "array" in the "Clue_datatype" cell, and the text of your tag in the "Clue_value" cell. 
3. If you don't want the data from a Spot On field to show up in your Clue data, you can simply delete it.  

There are some Spot on fields I included in the default mapping that you might want to adjust to your preferences:
- "ActionSick" defaults to "allergy_ailment". You'll see there are other options under "ailment" for Clue that you can move this to. Alternatively, you can make it a tag (see step 2) or delete it.
- "ActionHadSex" defaults to "protected". Other options you can choose are "unprotected" and "withdrawal". Alternatively you can make it a tag or delete it altogether.
- "ActionExercised" defaults to a tag. Clue offers four specific types of exercise in rows 30-33 that you can choose from if your exercise if predominantly one of these. Move "ActionExercised" to the blank cell of your choice. (You can edit individual days after you've imported your data into Clue.)
- "ActionSleptWell" and "ActionCouldntSleep" could also map to more specific fields in the sleep category, if you prefer.

Check all of the other mappings to make sure they're to your liking and move them around if you need, but make sure not to edit anything the "Clue_*" cells unless its a tag.  Once you've finished make sure that every Spot On field with a value also has values next to it in the "Clue_field", "Clue_datatype" and "Clue_value" columns. Now export your spreadsheet as a CSV file and name it the same as the CSV you imported, "my_spoton-to-clue_mapping.csv". When you're finished, it should look something like [this](https://github.com/saverkamp/spoton-data-conversions/blob/master/sample_edited_spoton-to-clue_mapping.csv). Save this file to your GitHub folder.  

### Create your new data import (Drip)  
If you've already started using Drip (Android only right now), when you go to import your data, the app will prompt you to either add your import data to your existing Drip data or overwrite all your existing Drip data with your import. If you have overlapping days between Spot On and Drip, you can include your Drip export in the Spot On data conversion to combine the daily data from both apps. Even if you don't want to combine your data exports, you should save a copy of your Drip export just in case the import doesn't work and you need to restore it. To export your Drip data, go to "settings" > "manage your data" then click "Export data". Make a copy of this file and put one in a safe place and put the other in the GitHub folder. (The file should be named "My drip data export.csv".)  

Run the "convert_spoton_data_to_drip.py" script in the terminal or command line with the following command. If you are combining your existing Drip data with your Spot On data, include the word "combine" in your command. You can also specify if you would like Drip to count spotting as part of your period with the word "include" (Spot on excludes spotting from your period while Drip gives you the option for each instance. This script excludes spotting by default.) 

Combine Spot On and Drip data:  
`python3 convert_spoton_data_to_drip.py combined`  

Combine Spot On and Drip data and count spotting as period:  
`python3 convert_spoton_data_to_drip.py combined include`

Don't combine data but count spotting as period:  
`python3 convert_spoton_data_to_drip.py include`  

Don't combine data and exclude spotting from period:  
`python3 convert_spoton_data_to_drip.py`  

If the conversion was successful, you should see a new file in the GitHub folder called "new_drip_import.csv" To import your data, put this file in your Google Drive or a location you can access from your phone. If you combined your data with your existing Drip export, select "Import and delete existing". Otherwise, select an option to either delete all of your Drip data and replace with your import file ("Import and delete existing") or keep your existing Drip data and replace only the days in the import file ("Import and replace"). Navigate to the import file on your phone, select it, and check your Drip history to make sure everything imported correctly. Once you've imported your data, you can edit individual days as needed.  

### Create your new data import (Clue)  
The Clue import will overwrite all existing data, so if you've already started using Clue, then first export your data by going to the settings menu, then "Backup/Restore" then "Back up data". Make a copy of this file and put one in a safe place and put the other in the GitHub folder.  

Run the "convert_spoton_data_to_clue.py" script in the terminal or command line with the following command. If you want to combine your existing Drip data with your Spot On data, include the word "combine" in your command. If you want to preference your Clue data for overlapping days, include the word "clue" in your command. If you want to preference your Spot On data for overlapping days, include the word "spoton". Your Clue export file includes the date of the export, so you will also need to include the filename in the command.  

Combine Spot On and Clue data:  
`python3 convert_spoton_data_to_clue.py combined ClueBackup-2020-03-25.cluedata`  

Preference Clue data over Spot On for overlapping days:  
 `python3 convert_spoton_data_to_clue.py clue ClueBackup-2020-03-25.cluedata`   

Ignore Clue backup data file:  
`python3 convert_spoton_data_to_clue.py`   

If the conversion was successful, you should see a new file in the GitHub folder called "new_clue_import.cluedata" To import your data, put this file in your Google Drive or a location you can access from your phone. Navigate to the import file on your phone, open it with Clue, and check your Clue history to make sure everything imported correctly. Once you've imported your data, you can edit individual days as needed. 
