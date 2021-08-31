# Co Location Rule
This is the code to calculate co-location rule. It's not even close to perfect since it just able to calculte for 2 items combinations.
I made it to help me calculate for my research. Feel free to use this code and I'll be happy if you can contribute too.

## How the code works
The data is should be clustered before, and in this code, the cluster column is named as 'Kecamatan' which can be defined as district in Indonesia.
It will check all unique categories for each cluster and then iterate the combinations.
No same category will be calculated for distance, since this code's objectives is calculating participation index between 2 categories in co-location rule.

## Usage
```python
# Importing the package
from co_location_rule import CoLocation

# or you can just directly copy the code in co_location_rule.py and paste into your .py file or jupyter notebook
```

Your initial data should be a Dataframe. It should be at least containing columns as follows

ID | Category | Kecamatan | Latitude | Longitude
--|--|--|--|--
*data type* `str` | *data type* `str` | *data type* `str` | *data type* `float` | *data type* `float`


Start the calculation by doing as follows:
```python

your_initial_data = pd.read_csv('file_name')    # any kind of read method should do great, just choose that suits you
                                                # or you can create a new dataframe from scratch

your_object_name = CoLocation(your_initial_data)  # it will takes much time depending the size of your data
```
For my case, my data has 2989 rows, 6 categories, and 38 kecamatan (districts).
It took me 20 minutes to run the code above.

After it finished, you should filter out the distance you decide.
For example, if you just want all distances within 2 kilometers, put 2 inside the method range_distance()
```python
your_object_name.range_distance(2)
```

To calculate the Participation Ratio and Participation Index, call method count_co_location()
```python
your_object_name.count_co_location()
```

The final calculations can be shown by calling this method
```python
your_object_name.co_location_result()     # Returning all calculated Participation Ratio and Participation Index

your_object_name.co_location_pruned()     # Returning a filtered Participation Index above 50%
```

The returned dataframe after calling the method above is looked like below:

Category 1 | Category 2 | PR 1 | PR 2 | PI
--|--|--|--|--
*data type* `str` | *data type* `str` | *data type* `float` | *data type* `float` | *data type* `float`



# License
MIT License

Copyright (c) 2021 Felix Malvian

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
