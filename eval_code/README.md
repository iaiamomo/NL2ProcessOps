## Code generation evaluation
Evaluated over a set of 10 textual process description with relative manual generated Python function implementations ([data](data)).

### Results
$CodeBLEU=\alpha \cdot BLEU+\beta \cdot BLEU_{weight} + \gamma \cdot Match_{ast} + \delta \cdot Match_{df}$ \
$BLEU=$ n-grams comparison between the candidate and the reference, and calculates the ratio of matched n-grams\
$BLEU_{weight}=$ weighted n-grams match \
$Match_{ast}=$ syntactic AST match \
$Match_{df}=$ semantic data flow match

CodeBLEU weights `(0.1, 0.1, 0.4, 0.4)`


#### With pre-processing ([run1](run1))
```
  model process  codebleu      bleu  bleu_weight  match_ast  match_df
0  gpt4     p01  0.615587  0.092619     0.220428   0.682927  0.777778
1  gpt4     p02  0.747616  0.125247     0.531403   0.804878  0.900000
2  gpt4     p03  0.607658  0.116968     0.315726   0.673267  0.737705
3  gpt4     p04  0.504420  0.092167     0.157967   0.653061  0.545455
4  gpt4     p05  0.622552  0.052832     0.316228   0.736842  0.727273
5  gpt4     p06  0.676450  0.176358     0.493827   0.737864  0.785714
6  gpt4     p07  0.674258  0.028473     0.179518   0.716981  0.916667
7  gpt4     p08  0.604011  0.053132     0.274819   0.653846  0.774194
8  gpt4     p09  0.557447  0.022540     0.099360   0.653465  0.709677
9  gpt4     p10  0.547670  0.041290     0.143339   0.651376  0.671642
```
```
codebleu: 0.615767
bleu: 0.080163
bleu_weight: 0.273261
match_ast: 0.696451
match_df: 0.75461
```

#### With pre-processing + distinct models ([run2](run2))
```
  model process  codebleu      bleu  bleu_weight  match_ast  match_df
0   gpt     p01  0.643492  0.088415     0.268456   0.719512  0.800000
1   gpt     p02  0.706665  0.149033     0.498103   0.804878  0.800000
2   gpt     p03  0.597559  0.092326     0.291320   0.693069  0.704918
3   gpt     p04  0.489725  0.112397     0.163638   0.666667  0.488636
4   gpt     p05  0.631017  0.044390     0.304056   0.763158  0.727273
5   gpt     p06  0.664707  0.189857     0.460677   0.766990  0.732143
6   gpt     p07  0.608050  0.027695     0.184882   0.716981  0.750000
7   gpt     p08  0.639535  0.114157     0.415188   0.692308  0.774194
8   gpt     p09  0.607898  0.025035     0.055865   0.693069  0.806452
9   gpt     p10  0.427459  0.035767     0.144612   0.486239  0.537313
```
```
codebleu: 0.601611
bleu: 0.087907
bleu_weight: 0.27868
match_ast: 0.700287
match_df: 0.712093
```

#### Without pre-processing ([run3](run3))
```
  model process  codebleu      bleu  bleu_weight  match_ast  match_df
0  gpt4     p01  0.568128  0.056919     0.137102   0.682927  0.688889
1  gpt4     p02  0.747317  0.122253     0.531403   0.804878  0.900000
2  gpt4     p03  0.613435  0.092765     0.292522   0.683168  0.754098
3  gpt4     p04  0.539187  0.066545     0.185867   0.659864  0.625000
4  gpt4     p05  0.636456  0.102660     0.300182   0.763158  0.727273
5  gpt4     p06  0.666119  0.147222     0.419657   0.737864  0.785714
6  gpt4     p07  0.585705  0.027634     0.179518   0.773585  0.638889
7  gpt4     p08  0.593877  0.069306     0.286342   0.653846  0.741935
8  gpt4     p09  0.537324  0.015101     0.053762   0.584158  0.741935
9  gpt4     p10  0.559952  0.050291     0.142139   0.605505  0.746269
```
```
codebleu: 0.60475
bleu: 0.075069
bleu_weight: 0.252849
match_ast: 0.694895
match_df: 0.735
```

#### Without pre-processing + distinct models ([run4](run4))
```
  model process  codebleu      bleu  bleu_weight  match_ast  match_df
0   gpt     p01  0.632569  0.116853     0.268456   0.707317  0.777778
1   gpt     p02  0.644222  0.125009     0.390381   0.731707  0.750000
2   gpt     p03  0.572925  0.089821     0.283801   0.683168  0.655738
3   gpt     p04  0.534736  0.080603     0.145546   0.666667  0.613636
4   gpt     p05  0.640185  0.107422     0.437972   0.736842  0.727273
5   gpt     p06  0.658486  0.113583     0.338129   0.747573  0.785714
6   gpt     p07  0.663541  0.027052     0.184882   0.716981  0.888889
7   gpt     p08  0.606151  0.066354     0.335111   0.673077  0.741935
8   gpt     p09  0.607565  0.023807     0.053762   0.693069  0.806452
9   gpt     p10  0.475843  0.042625     0.102905   0.541284  0.611940
```
```
codebleu: 0.603622
bleu: 0.079313
bleu_weight: 0.254094
match_ast: 0.689769
match_df: 0.735936
```

#### Without process model ([run5](run5))
```
  model process  codebleu      bleu  bleu_weight  match_ast  match_df
0  gpt4     p01  0.474711  0.073180     0.124334   0.670732  0.466667
1  gpt4     p02  0.757547  0.118564     0.530082   0.731707  1.000000
2  gpt4     p03  0.573000  0.194563     0.468077   0.693069  0.573770
3  gpt4     p04  0.435810  0.031333     0.087121   0.639456  0.420455
4  gpt4     p05  0.598079  0.100604     0.339513   0.657895  0.727273
5  gpt4     p06  0.599895  0.216807     0.414600   0.699029  0.642857
6  gpt4     p07  0.543521  0.039103     0.171791   0.528302  0.777778
7  gpt4     p08  0.574228  0.062993     0.274819   0.576923  0.774194
8  gpt4     p09  0.525575  0.015806     0.039688   0.574257  0.725806
9  gpt4     p10  0.396067  0.061120     0.099470   0.532110  0.417910
```
```
codebleu: 0.547843
bleu: 0.091407
bleu_weight: 0.254949
match_ast: 0.630348
match_df: 0.652671
```

#### Copilot ([copilot](copilot))
```
     model process  codebleu      bleu  bleu_weight  match_ast  match_df
0  copilot     p01  0.408391  0.109266     0.179527   0.548780  0.400000
1  copilot     p02  0.279168  0.035970     0.082540   0.268293  0.400000
2  copilot     p03  0.272242  0.028794     0.047955   0.366337  0.295082
3  copilot     p04  0.444315  0.056221     0.074312   0.612245  0.465909
4  copilot     p05  0.425849  0.130979     0.318897   0.315789  0.636364
5  copilot     p06  0.369029  0.028167     0.052550   0.563107  0.339286
6  copilot     p07  0.382015  0.002500     0.010526   0.396226  0.555556
7  copilot     p08  0.344252  0.032626     0.064977   0.384615  0.451613
8  copilot     p09  0.488768  0.009509     0.016461   0.683168  0.532258
9  copilot     p10  0.351872  0.049003     0.129174   0.596330  0.238806
```
```
codebleu: 0.37659
bleu: 0.048303
bleu_weight: 0.097692
match_ast: 0.473489
match_df: 0.431487
```