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
0  gpt4     p01  0.618003  0.087548     0.249664   0.682927  0.777778
1  gpt4     p02  0.644222  0.125009     0.390381   0.731707  0.750000
2  gpt4     p03  0.577924  0.100565     0.309415   0.702970  0.639344
3  gpt4     p04  0.468172  0.046792     0.113595   0.653061  0.477273
4  gpt4     p05  0.644744  0.049710     0.330739   0.789474  0.727273
5  gpt4     p06  0.677942  0.191277     0.493827   0.737864  0.785714
6  gpt4     p07  0.643919  0.026971     0.179518   0.641509  0.916667
7  gpt4     p08  0.593850  0.034754     0.166777   0.692308  0.741935
8  gpt4     p09  0.599742  0.012098     0.051759   0.693069  0.790323
9  gpt4     p10  0.566027  0.068204     0.176208   0.697248  0.656716
```
```
codebleu: 0.603455
bleu: 0.074293
bleu_weight: 0.246188
match_ast: 0.702214
match_df: 0.726302
```

#### With pre-processing + distinct models ([run2](run2))
```
  model process  codebleu      bleu  bleu_weight  match_ast  match_df
0   gpt     p01  0.669592  0.082751     0.268456   0.719512  0.866667
1   gpt     p02  0.609555  0.058848     0.397681   0.609756  0.800000
2   gpt     p03  0.607586  0.116243     0.315726   0.673267  0.737705
3   gpt     p04  0.464389  0.062014     0.142483   0.666667  0.443182
4   gpt     p05  0.640627  0.064357     0.380188   0.763158  0.727273
5   gpt     p06  0.681955  0.150504     0.464469   0.747573  0.803571
6   gpt     p07  0.650640  0.031976     0.268977   0.773585  0.777778
7   gpt     p08  0.680574  0.070118     0.408077   0.807692  0.774194
8   gpt     p09  0.607565  0.023807     0.053762   0.693069  0.806452
9   gpt     p10  0.455867  0.045072     0.148813   0.568807  0.522388
```
```
codebleu: 0.606835
bleu: 0.070569
bleu_weight: 0.284863
match_ast: 0.702309
match_df: 0.725921
```

#### Without pre-processing ([run3](run3))
```
  model process  codebleu      bleu  bleu_weight  match_ast  match_df
0  gpt4     p01  0.591154  0.063429     0.174399   0.707317  0.711111
1  gpt4     p02  0.642559  0.106952     0.391808   0.731707  0.750000
2  gpt4     p03  0.595523  0.100456     0.302431   0.683168  0.704918
3  gpt4     p04  0.501788  0.123019     0.173461   0.646259  0.534091
4  gpt4     p05  0.639027  0.110315     0.318236   0.763158  0.727273
5  gpt4     p06  0.656853  0.158581     0.419657   0.747573  0.750000
6  gpt4     p07  0.591624  0.012008     0.080328   0.622642  0.833333
7  gpt4     p08  0.606998  0.058193     0.274819   0.692308  0.741935
8  gpt4     p09  0.537268  0.014538     0.053762   0.584158  0.741935
9  gpt4     p10  0.526917  0.039957     0.143634   0.614679  0.656716
```
```
codebleu: 0.588971
bleu: 0.078745
bleu_weight: 0.233254
match_ast: 0.679297
match_df: 0.715131
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
0  gpt4     p01  0.462886  0.046684     0.112798   0.695122  0.422222
1  gpt4     p02  0.601784  0.099717     0.474224   0.560976  0.800000
2  gpt4     p03  0.506447  0.108476     0.271041   0.613861  0.557377
3  gpt4     p04  0.483498  0.066225     0.138267   0.646259  0.511364
4  gpt4     p05  0.596853  0.088346     0.339513   0.657895  0.727273
5  gpt4     p06  0.600812  0.222318     0.418253   0.699029  0.642857
6  gpt4     p07  0.566377  0.041250     0.171791   0.584906  0.777778
7  gpt4     p08  0.717689  0.057334     0.275886   0.807692  0.903226
8  gpt4     p09  0.525277  0.034384     0.053267   0.613861  0.677419
9  gpt4     p10  0.420370  0.042289     0.145530   0.541284  0.462687
```
```
codebleu: 0.548199
bleu: 0.080702
bleu_weight: 0.240057
match_ast: 0.642089
match_df: 0.64822
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