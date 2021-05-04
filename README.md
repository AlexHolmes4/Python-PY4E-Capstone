

<h1>PY4E - CAPSTONE PROJECT</h2>

<h2>Overview</h2>
For the final (optional) assignment of the PY4E specalization students were to pick a data source, analyse it and visually represent patterns. I chose <a href = https://academictorrents.com/details/a2ccf94bbb4af222bf8e69dad60a68a29f310d9a> flight data from academic torrents </a>. This data was too large to upload to the GitHub repository reliably, but you can download from the source link above as a tsv file. 


<h3>"High Level Solution Architecture"</h3>

![flightdatacrawler High Level Overview](https://user-images.githubusercontent.com/55677663/116178867-d9e3c900-a748-11eb-8f0f-f5dbab3d3708.PNG) 

<ul>
  <li> A python program will run and extract the data into a raw storage database. This first extraction of data is unstructured, the stopping and restarting of data extraction will be incorporated in the python program - SQL query design. </li>
  <li> The data can be processed, modelled and stored into a second structured relational database where querying is optimized. </li>
  <li>This data can now visualized using Javascript. The D3 (Data Driven Documents) Javascript Library was chosen for the visualisation. </li>
 </ul>
 
 <h3>Solution Architecture - Multi Layered Analysis</h3>

![flightdatacrawler High Level Solution](https://user-images.githubusercontent.com/55677663/116178864-d81a0580-a748-11eb-8cce-ed0ca93e058b.PNG)

<h3>Data Model</h3>

![data model flights](https://user-images.githubusercontent.com/55677663/116188803-93976580-a75a-11eb-9730-d054eab357a9.PNG)

<h3>Screenshots of The Process and End Results</h3>

**First**  `fgather.py` was used to retrieve the data source and insert it into a raw unstructured database (`rawfdata.sqlite`)
A method to stop and continue retrieving where the program left off was introduced to handle large data retrieval. 

![gather](https://user-images.githubusercontent.com/55677663/116570913-34457b00-a93d-11eb-8413-d66d8a61b127.PNG)

__Next__ the data needed to be restructured, so the raw database was retrieved by `fmodel.py` and inserted into a new relational database, optimized for data retrieval.
Again a method was introduced to allow the program to pick up from where it left off if interruptions occur. 

![commandline fmodel](https://user-images.githubusercontent.com/55677663/116573106-1da02380-a93f-11eb-8ecd-00fa57580cb4.PNG)

![fstructured DB](https://user-images.githubusercontent.com/55677663/116573869-c2bafc00-a93f-11eb-9404-7708a2a1666e.png)

__Once__ the data was modelled it could be analysed, such as flights frequency plotted on a chart, or visualizing connections between cities.

<h3>Visualising The Data</h3>

![fbasic](https://user-images.githubusercontent.com/55677663/116577945-838eaa00-a943-11eb-8b81-1c24631ce2c7.PNG)

![flight line chart](https://user-images.githubusercontent.com/55677663/116580408-eda84e80-a945-11eb-890b-d2b1e581c62b.PNG)

![force lots of data](https://user-images.githubusercontent.com/55677663/116657880-bd05fa80-a9c1-11eb-9286-a0cae5fb216b.PNG)













