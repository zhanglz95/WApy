# WApy(Weiler-Atherton clipping algorithm in python)
This rep is python implementation of Weiler-Atherton clipping algorithm.

*Reference:*[https://www.cnblogs.com/lsxqw2004/p/4843417.html](https://www.cnblogs.com/lsxqw2004/p/4843417.html)

*Reference rep*:[https://github.com/lsxqw2004/blog_sample_codes](https://github.com/lsxqw2004/blog_sample_codes)


## How to use?
Just copy the python file into the path of your project and import:
```markdown
from PolygonCut import *
```

The two Polygons you input should be like this:
```markdown
#"x y x y ... x y" in clockwise by Default, otherwise transform to clockwise
S = "161 137 429 376 558 192 619 418 281 431"
C = "183 391 224 240 610 107 657 361 429 376"
```

Then get the clipped Polygons:
```markdown
result = PolyClipping(S, C)			# True by default
#result = PolyClipping(S, C, False) # if you want anticlockwise output
```

The format of result should be like this:
```markdown
#"x y x y ... x y" in clockwise by Default
["261.867222 226.952486 429.000000 376.000000 262.690141 386.140845 215.627162 270.836548 224.000000 240.000000",
"429.000000 376.000000 558.000000 192.000000 604.546479 364.450890"]
```

**Moreover：**
The coordinate frame is:

------------------------------------>*x+*    
|    
|    
|    
|    
|    
|    
|    
|    
|    
v    
*y+*    