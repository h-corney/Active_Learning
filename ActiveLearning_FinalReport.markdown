Michael Agboola, Hannah Corney

Meyru Bhanti & Alex Shaller

Final Report

New Methods in EO

**Active Learning: Mapping Agricultural Fields in Ghana**

**1.0 Introduction:** What is the overall aim of the project and what
specific Earth Observation is it trying to solve?

Machine learning algorithms are able to use relatively small training
sets to find spectral patterns in diverse areas of interest creating
classification. Computers are unparalleled in their pattern recognition
ability. However machine learning can be inflexible when it comes across
the natural variability in a particular land cover class. According to
Russell & Norvig (2009), Artificial intelligence (AI) can be described
as an act whereby a machine tries to imitate complex functions of human
minds to learn and resolve problems. As an application of AI, machine
learning gives the ability to understand a particular pattern of a
phenomenon and improving on the observed patterns without entirely
automating the process involved in it. It also offers giant advancements
within the field of earth observation. Over larger areas of interest it
can be difficult and time consuming to create sufficient training sites
which capture all the nuance of particular land cover class.

Active learning seeks to fill this gap by pairing the efficient pattern
recognition of computers with the human ability to recognize the
variation with particular land cover classes. Active learning is a
special case of machine learning in which a learning algorithm is able
to interactively query the user (or some other information source) to
obtain the desired outputs at new data points. The iterative approach to
creating training sites allows for the human judgment to improve the
machine learning. Furthermore active learning provides an opportunity to
utilize vast human knowledge of a particular scene through
crowdsourcing. In particular to this project, it was adopted in querying
the mapping process to obtain the desired output which is identifying
the crop fields in Ghana.

**1.1 Aim & Objectives**

This project aims at utilizing both open source and land cover mapping
platform to optimally use human judgement to guide machine learning
approach in data collected. To attain the aim of this project, the
stated objective are:

a.  To distinguish agricultural from non-agricultural areas with
    unprecedented accuracy,

b.  Use pixel-based classifications to map individual fields,

c.  Combined human-machine approach to overcome obstacles in mapping
    complex agricultural landscapes.

**1.2 Study Area & Data **

The study area for this project is located in the northern region of
Lake Volta in the Eastern part of Ghana (West Africa). It covers
approximately 99.256 km^2^, and is identified to be vastly dominated
with agricultural crop fields. Using archived data acquired by
commercial satellite fleets, the Planet data which is aggregated by
growing and off-growing seasons were used in this project. Based on
these two season adopted, four (4) different Planet data were used for
the mapping exercise namely;

I.  Growing season False Color

II. Growing season True Color

III. Off-season False Color

IV. Off-season True Color

**2.0. Methods:** What were the methods you developed and/or applied?
(H.C for 2.0 - 2.3)

A major portion of this project's methodology was related to setting up
a new instance of the mapping platform for our AOI in Ghana. This
involved three major steps which are outlined in more detail below.
Initially, each member needed to generate an SSH key in order to
securely access the server. For a Mac user, this can be generated in the
Terminal by running

ls \~/.ssh/\*/pub

Followed by

cat \~/.ssh/id\_rsa.pub

For a Windows user, this was done using either Cygwin or Putty.

**2.1 Planet Downloader**

Downloading Planet imagery requires a number of configuration files and
permissions. A more detailed description of the steps involved can be
found [here.](https://github.com/agroimpacts/mapperAL/blob/devel/spatial/python/planet/README.md)

however a simplified outline of the steps for our project are defined
below.

The config.ini.template is the first thing that needed to be edited,
which is found [here.](https://github.com/agroimpacts/mapperAL/spatial/python/planet/cfg/config.ini.template)

Information such as the API key for the Planet account, the path to the
AOI in the form of a geojson file, and output s3 bucket directory in AWS
(among other parameters) were updated for our instance.

Next, a local Docker image and container must be created, which requires
downloading [Docker.](https://www.docker.com/get-started)

Then, the Docker container must be pushed to AWS using;

dockerpush554330630998.dkr.ecr.us-east-1.amazonaws.com/planet-downloader:my-fancy-tag

With the "my-fancy-tag" replaced with the tag of the Docker container
just created. Once the AWS Permissions and passwords have been
configured, the planet downloader is then ready to be executed.

**2.2 Migrate Mapper**

Migrating Mapper involves transferring the information in the database
from development phase in production phase (from AfricaSandbox to
Africa). Details on this process can be found [here](https://github.com/agroimpacts/mapperAL/blob/devel/docs/migrating-mapper.md)

and our steps can be found below.

The generateUpdateConfigurationSandbox.sh script creates another file
called updateConfigurationSandbox.sql. The contents from this file
should be copied into a new file called updateConfiguration.sql, where
the specific parameters for the instance can be changed. For example, in
our instance, we only had 4 mappers, therefore the number of F sites
that needed to be classified in order to count towards the machine
learning algorithm (CVML) was changed to 2. The accuracy threshold was
also lowered from .6 to .4 for our team. These parameters were edited in
a Mac terminal using VIM to edit the file actively. After that was
complete, the migrate.sh script performs the migration with the updated
information into the appropriate database location.

**2.3 Mapper in production**

Mapper in production is used to connect the instance with our AOI,
connect to CVML, and generate the first selection of F sites for our
team to map. The first step is to configure mapper to work with CVML,
which involved running the fire\_up\_mapper.py script. This has
parameters within that need to be edited, such as the AWS passwords, the
overall AOI and appropriate s3 bucket directory. The region for the
first selection of F sites needs to be specified, which is done by
running the Rscript spatial/R/create\_f\_pool.py 6 script, which selects
the 6th polygon generated by the create\_f\_pool script as a target
geography. It creates a unique AOI from that geography, which needs to
be re-inserted into the fire\_up\_mapper script which will orient the F
sites to that region. Finally, the python common/initial\_f\_sites.py
script will generate the first F sites to be classified. More detail on
this process can be found [here](https://github.com/agroimpacts/mapperAL/blob/devel/docs/running-mapper-in-production.md)

**2.4 Active Learning**

During iteration zero 40 F sites were mapped and approximately 10 Q
sites. During each subsequent iteration 10 F sites were mapped and the
training data was added to the random forest classification. After each
iteration the areas of the lowest classification accuracy, which is
determined from the p value of the pixel, was used to determine the next
set of F sites. Once the instance was set up properly we monitored the
worker and iteration accuracy. During each iteration approximately 10%
of the sites where Q sites which allowed us to monitor the worker
accuracy. During this phase our focus was on properly mapping enough
sites for the iteration to run and the code was not modified. After 6
iterations the active learning loop was stopped and analyzed.

**2.5 Accuracy Assessment (methods)** (AS)

A skill statistic measure was used to determine the accuracy after each
iteration. The True Skill Statistic is based on true positives TP
(correctly identifying that there is a field at a given location), true
negatives TN (correctly identifying that there is not a field at a given
location), false positives FP (falsely identifying that there is a field
at a given location) and false negatives FN (failing to identify that
there is a field at a given location). The formula for true skill
statistic is TSS = TPR + TNR -- 1, where TPR = TP/ (TP + FN) and TNR =
TN/ (TN + FP). TSS ranges from -1 to 1, where 0 would indicate that the
workers have no skill (they are no better at identifying fields that a
random generator).

The composite training maps are created where each individual field
mapping is weighted by the individual's overall average accuracy.
Bayesian merging was used to create a composite map based on each
worker's mappings that takes into account the overall average accuracy
of each of the workers.

Several dimensions of accuracy are assessed to determine a quality score
for each map for each worker. In particular, the quality score is based
primarily on identifying true positives and true negatives correctly for
the fields, but it's also in part based on identifying the correct
number of fields. In other words if there are two separate fields that
are mapped together as one field by the worker, his accuracy will be
lower than if they are mapped correctly as two fields separately by the
worker. Image segmentation is the technique used to back out where the
fields are from the composite map, and these are used for training a CNN
(convolutional neural network), according to the documentation of
github. Image segmentation is a commonly used remote sensing technique.

**2.3 Probability Analysis** (MB)

Probability images were randomly selected and were made up of multiple
cells. Values in each cells ranged from 0%- 100% of being a crop field.
Each probability image was reclassified into high (66%-100%) medium
(33%-66%) and low probability (0%- 33%). The reclassed images from
iteration 0 and iteration 6 were then analyzed using cross tab.

Analysis: What were your results?

**3.0 Worker accuracy/Classification accuracy** (AS)



![](https://github.com/h-corney/Active_Learning/Accuracy_by_iteration.png)

The bar graph above shows the average accuracy for each iteration which
was calculated using the Q sites. There is a significant increase in
accuracy between the first two iterations. Between iterations 2 and 6
the accuracy plateaued around 0.68. This result was similar to those
obtained previously by the Kenyan research group. Though it was beyond
the scope of this project, future work should try to understand what
caused the plateau in classification.

The TSS scores for each iteration of our mappings are shown in the
following table:

Table 1: The TSS by iteration for our team:

  ----------- ----------- ----------- ---------- ---------- ---------- ----------
  Iteration   1           2           3          4          5          6
  TSS         0.0161489   0.0833947   0.113155   0.115918   0.109304   0.114229
  ----------- ----------- ----------- ---------- ---------- ---------- ----------

A key difference between our analysis and the Kenyan team is that we
only have 2 people digitizing each particular site and not 5. This could
have lead to lower accuracy rates for us. However, our overall accuracy
of around 68% is consistent with the Kenyan team.

**3.1 Probability Images** (MB)

![](https://github.com/h-corney/Active_Learning/Prob_Images_1.png)

Figure 1: This is an example of a cross tab image that was generated for
all intermediate probability images. The left side of the legend shows
the probability in iteration 1 and the second side of the legend shows
the probability in iteration 6.

Table 2: The probability transition between iteration 1 and 6 over all
cells in the probability image.

  ------------------------ ------------------------------------------------- -------------
  Probability transition   Total number of cells in all probability images   Percentage
  High \| High             271372                                            1.476676337
  Medium \| High           106136                                            0.577541234
  Low \| High              29728                                             0.161765525
  High \| Medium           80100                                             0.435865803
  Medium \| Medium         153328                                            0.834337475
  Low \| Medium            166824                                            0.907776238
  High \| Low              32700                                             0.177937725
  Medium \| Low            256708                                            1.396881878
  Low \| Low               17280320                                          94.03121779
  4 \| 4                   115840512                                         630.3485359
  Sum:                     18377216                                          100
  ------------------------ ------------------------------------------------- -------------

The probability images the crosstab of iteration 1 and iteration 6 were
interpreted. The first iteration of the random forest classification was
fairly strong at classifying the agricultural fields. 94% of the cells
remained low probability of being an agricultural field (3:3) in
iteration 1 and iteration 6. The second highest percentage of cells were
areas of high probability of being a field in iteration 1 and 6 (1.47%).

![](https://github.com/h-corney/Active_Learning/Transitions.png)


The iterative approach to training sites allowed the algorithm to refine
classification of non agricultural fields. The highest percentage of
cells that changed probability from iteration 1 to iteration 6 changed
from areas of medium probability to low probability of being an
agricultural field. The second highest transition was from low
probability to medium probability.

**3.2 Final Classification of AOI** (MB)

![](https://github.com/h-corney/Active_Learning/Final_AOI.png)

Figure 2: The final classification over the area of interest. The black
areas show the areas of no images downloaded.

Table 2:The probability of being an agricultural field over all area
classified.

  ------------------------ ------------
  Land Cover Probability   Percentage
  High Probability         11%
  Medium Probability       17%
  Low Probability          72%
  ------------------------ ------------

In the final classification, the entire area of interest was not
classified due to the imagery not being available in some places. The
red areas in figure 2 shows the areas of high probability of being an
agricultural field while green shows the areas of low probability of
being an agricultural field. There seems to be some disparity in
classification over all images. In the lower left side of the image,
there are some areas with high probability of being an agricultural
field with an unnatural transition to images of low probability of being
an agricultural field. The final classification of the active learning
classified 11% of the study area as being a high probability of being an
agricultural field.

**4.0 Conclusions** ( Did the results show that the project aim was
realized?)

The classification of agricultural fields increased in accuracy from
iteration 1 to iteration 6 over most of the study area, though overall
the classification did not improve uniformly over all probability
images.

We were able to classify most of the study area of Ghana based on
probability of being a cropfield. However, our measured accuracy and
skill were far from perfect. The amount of computing time spent by
computing resources and the amount of work digitizing fields were
relatively low, and there were no additional costs. (AS)

Was an Earth Observation limit pushed back (or potentially pushed back)?

Our group project demonstrates that active learning is a viable
methodology to push back the current limits on earth observation. The
iterative process of creating training sites pushes back both temporal
and spatial limitations of remote sensing by allowing large areas to be
classified in a relatively short amount of time. According to Debats
(2017), using active learning with crowdsourcing to do crop mapping
saves immensely on resources, both time and money. They suggest that the
entire continent of Africa can feasibly be mapped relatively cheaply in
the near future using an active learning approach. (AS) The crowd
sourcing component of the methodology allowed different workers to
collaborate, and overall provides more accurate training data free of
the biases of a single worker. This project also pushes back on remote
sensing as being an esoteric field; by using active learning, this
integrates non-experts of remote sensing into the classification
process, therefore removing some of the "expertise barrier" that remote
sensing often creates. (HC)

If this was a group project, how were the results of individual efforts
integrated?

For this project the group supported one another in understanding the
process of Active learning and all individual efforts were integrated in
our analysis of the outputs.

Future Work: What are potential improvements, and any next steps you
plan to take? (AS)

Future work could seek to understand why the accuracy of the iterations
plateaued after iteration 2. We could have done more during the
digitizing phase to understand how to improve our accuracy, in between
iterations. For example, we could have determined when we should rely on
the false color composite map layer versus the true color composite map
layer. To improve our accuracy for a future project, we could try out
different strategies and determine what is more likely to result in
higher accuracy scores.

Our project differentiates between where there is a field and where
there is no field. It would be great if we could use active learning to
differentiate between the different crops that are grown in Africa or to
differentiate different landscapes or different densities of vegetation.
Another future project idea would be to map a larger geographic area
with diverse landscapes.

**REFERENCE**

Russell, Stuart J.; Norvig, Peter (2009). Artificial Intelligence: A
Modern Approach (3rd ed.). Upper Saddle River, New Jersey: Prentice
Hall. ISBN 0-13-604259-7.

Debats, SR, Estes LD, Thompson DR, Caylor KK (2017) Integrating active
learning and crowdsourcing into large-scale supervised landcover mapping
algorithms. PeerJ Preprints 5:e3004v1
[[https://doi.org/10.7287/peerj.preprints.3004v1]{.underline}](https://doi.org/10.7287/peerj.preprints.3004v1).
