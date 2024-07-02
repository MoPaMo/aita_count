# Reddit AITA Historical Analysis Bot

AITA Analyzer is an application designed to gather and analyze data from the subreddit r/AmItheAsshole. 

### Method
The app gahters the 1k top posts (either from all time or the last year).
It then extracts the top comment from each post and looks for either NTA, YTA<, ESH or NA. If it doesn't find one of these flags in the top comment, it scans the next top comment in the post. 

### Limitations
This means that the data in this website may not be 100% accurate, as it only considers 1. the top comment in each post and 2. the highest ranking posts.
It is not possible to gather more data, as Reddit imposes restrictions that allow you to only collect up to 1000 posts at once.
