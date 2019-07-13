# pyoklock
python cli clock. Display digital clock on terminal.

![screenshot](https://github.com/6syun9/pyoklock/blob/master/images/screenshot.png?raw=true)

# Usage

## install
```
pip install pyoklock
```

## args: second
If you want display `second`, add `-s` or `--second` to the argument.
```
pyoklock -s
```


## args: frame
If you want display clock frame, add `-f` or `--frame` to the argument.
```
pyoklock -f
```
![screenshot](https://github.com/6syun9/pyoklock/blob/master/images/frame.png?raw=true)


## args: google_calender

If you want display Google Calender's moost recent event, add `-g` or `--google_calender` to the argument.
To use this args, you must get `Google API OAuth Client credentails`. 
If you got `credentails`, put it at `~/.pyoklock/` with the name `credentails.json`

OAuth Client credentails from: https://console.cloud.google.com/
```
mkdir ~/.pyoklock
mv [[your credentail path]] ~/.pyoklock/credentials.json
```

Then run pyoklock.
```
pyoklock -g
```

![screenshot](https://github.com/6syun9/pyoklock/blob/master/images/google_calender.png?raw=true)

If you want to delete the cache, remove `~/.pyoklock/token.pickle`.  
If you want to limit the number of events, using `--events` args.  
for example:
```
pyoklock -g --events 5
```


# Special thanks to
 - [python prompt-toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) : pyoklock made by this cli tools.

# License
This software is released under the MIT License, see LICENSE.txt.

# Why PyOkLock?

python clock. -> pyoklock  
This is the same way as the artist " [ONE OK ROCK](http://www.oneokrock.com) "  I respect.
