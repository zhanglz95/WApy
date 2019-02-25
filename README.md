# WApy(Weiler-Atherton clipping algorithm in python)
This rep is python implementation of Weiler-Atherton clipping algorithm.

## How to use?
Just copy the python file into your project and "import" it:
```markdown
import PolygonCut
```

The two Polygons you input should like this:
```markdown
#"x y x y ... x y" in clockwise
S = "161 137 429 376 558 192 619 418 281 431"
C = "183 391 224 240 610 107 657 361 429 376"
```

Then get the clipped Polygons:
```markdown
result = PolyClipping(S, C)
```

The format of result should like this:
```markdown
#"x y x y ... x y" in clockwise
["261.867222 226.952486 429.000000 376.000000 262.690141 386.140845 215.627162 270.836548 224.000000 240.000000",
"429.000000 376.000000 558.000000 192.000000 604.546479 364.450890"]
```
