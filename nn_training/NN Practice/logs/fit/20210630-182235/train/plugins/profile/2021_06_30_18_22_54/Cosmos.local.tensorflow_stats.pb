"?I
BHostIDLE"IDLE1     @?@A     @?@a?r? ????i?r? ?????Unknown
?HostResourceApplyAdam""Adam/Adam/update/ResourceApplyAdam(1     ?a@9     ?a@A     ?a@I     ?a@ad6?????i??OҞE???Unknown
uHostFlushSummaryWriter"FlushSummaryWriter(1     ?U@9     ?U@A     ?U@I     ?U@a??#/??ikK??????Unknown?
sHostDataset"Iterator::Model::ParallelMapV2(1      R@9      R@A      R@I      R@a^>?ݎ??i^??e????Unknown
?HostDataset"?Iterator::Model::ParallelMapV2::Zip[0]::FlatMap[0]::Concatenate(1     @S@9     @S@A     ?Q@I     ?Q@aj.?W?a??iўE?????Unknown
wHost_FusedMatMul"sequential/BrainLayer/BiasAdd(1     ?G@9     ?G@A     ?G@I     ?G@a?v???
??i??̦Zc???Unknown
~HostMatMul"*gradient_tape/sequential/BrainLayer/MatMul(1      A@9      A@A      A@I      A@au??????i???????Unknown
?HostDataset"5Iterator::Model::ParallelMapV2::Zip[1]::ForeverRepeat(1      ?@9      ?@A      >@I      >@a????????i}??,???Unknown
?	HostRandomUniform"<sequential/DropoutLayer/dropout/random_uniform/RandomUniform(1      <@9      <@A      <@I      <@a????RN??ix??w;n???Unknown
i
HostWriteSummary"WriteSummary(1      5@9      5@A      5@I      5@a??|u~?i?Ʈo&????Unknown?
?HostResourceApplyAdam"$Adam/Adam/update_1/ResourceApplyAdam(1      2@9      2@A      2@I      2@a^>?ݎz?i1?j?]????Unknown
^HostGatherV2"GatherV2(1      0@9      0@A      0@I      0@a??A??4w?i.?n????Unknown
?HostResourceApplyAdam"$Adam/Adam/update_3/ResourceApplyAdam(1      *@9      *@A      *@I      *@aҞE??r?il?5v}3???Unknown
dHostDataset"Iterator::Model(1     @U@9     @U@A      *@I      *@aҞE??r?i?5v}3Y???Unknown
zHostMatMul"&gradient_tape/sequential/Output/MatMul(1      (@9      (@A      (@I      (@a?~???gq?i???|???Unknown
lHostIteratorGetNext"IteratorGetNext(1      &@9      &@A      &@I      &@a?:??o?ifS???????Unknown
eHost
LogicalAnd"
LogicalAnd(1      &@9      &@A      &@I      &@a?:??o?i$??|Ի???Unknown?
?HostBiasAddGrad"3gradient_tape/sequential/Output/BiasAdd/BiasAddGrad(1      &@9      &@A      &@I      &@a?:??o?i???G?????Unknown
?HostResourceApplyAdam"$Adam/Adam/update_2/ResourceApplyAdam(1      $@9      $@A      $@I      $@a0~??,m?i`[?t?????Unknown
?HostBiasAddGrad"7gradient_tape/sequential/BrainLayer/BiasAdd/BiasAddGrad(1      "@9      "@A      "@I      "@a^>?ݎj?i?E?????Unknown
|HostMatMul"(gradient_tape/sequential/Output/MatMul_1(1      "@9      "@A      "@I      "@a^>?ݎj?i?/~??,???Unknown
gHostStridedSlice"strided_slice(1      "@9      "@A      "@I      "@a^>?ݎj?i\!G???Unknown
?HostDynamicStitch".gradient_tape/mean_squared_error/DynamicStitch(1       @9       @A       @I       @a??A??4g?i\!G^???Unknown
sHost_FusedMatMul"sequential/Output/BiasAdd(1       @9       @A       @I       @a??A??4g?i??|u???Unknown
[HostAddV2"Adam/add(1      @9      @A      @I      @a????RNd?i?7?Uʉ???Unknown
?HostDataset"OIterator::Model::ParallelMapV2::Zip[0]::FlatMap[0]::Concatenate[0]::TensorSlice(1      @9      @A      @I      @a????RNd?i????????Unknown
vHostAssignAddVariableOp"AssignAddVariableOp_2(1      @9      @A      @I      @a?~???ga?i??\?????Unknown
vHostCast"$sequential/DropoutLayer/dropout/Cast(1      @9      @A      @I      @a?~???ga?i??g?????Unknown
vHostReadVariableOp"Adam/Cast_3/ReadVariableOp(1      @9      @A      @I      @a0~??,]?i???'i????Unknown
`HostGatherV2"
GatherV2_1(1      @9      @A      @I      @a0~??,]?iG^>?????Unknown
?HostTile"5gradient_tape/mean_squared_error/weighted_loss/Tile_1(1      @9      @A      @I      @a0~??,]?iQ??Tk????Unknown
? HostDivNoNan"?gradient_tape/mean_squared_error/weighted_loss/value/div_no_nan(1      @9      @A      @I      @a0~??,]?i??Tk?????Unknown
?!HostCast"2mean_squared_error/weighted_loss/num_elements/Cast(1      @9      @A      @I      @a0~??,]?i?"Ёm	???Unknown
?"HostGreaterEqual",sequential/DropoutLayer/dropout/GreaterEqual(1      @9      @A      @I      @a0~??,]?ilK?????Unknown
~#HostAssignAddVariableOp"Adam/Adam/AssignAddVariableOp(1      @9      @A      @I      @a??A??4W?i??#???Unknown
V$HostSum"Sum_2(1      @9      @A      @I      @a??A??4W?i??#/???Unknown
[%HostPow"
Adam/Pow_1(1      @9      @A      @I      @a?~???gQ?i˦Zc?7???Unknown
v&HostAssignAddVariableOp"AssignAddVariableOp_4(1      @9      @A      @I      @a?~???gQ?i???=?@???Unknown
?'HostDataset"/Iterator::Model::ParallelMapV2::Zip[0]::FlatMap(1      T@9      T@A      @I      @a?~???gQ?iI???I???Unknown
`(HostDivNoNan"
div_no_nan(1      @9      @A      @I      @a?~???gQ?i?8??Q???Unknown
i)HostMean"mean_squared_error/Mean(1      @9      @A      @I      @a?~???gQ?iǉ?̦Z???Unknown
t*HostMul"#sequential/DropoutLayer/dropout/Mul(1      @9      @A      @I      @a?~???gQ?i??̦Zc???Unknown
v+HostMul"%sequential/DropoutLayer/dropout/Mul_1(1      @9      @A      @I      @a?~???gQ?iE{?l???Unknown
],HostCast"Adam/Cast_1(1       @9       @A       @I       @a??A??4G?i??G??q???Unknown
v-HostReadVariableOp"Adam/Cast_2/ReadVariableOp(1       @9       @A       @I       @a??A??4G?iEy??w???Unknown
t.HostAssignAddVariableOp"AssignAddVariableOp(1       @9       @A       @I       @a??A??4G?i?l?5v}???Unknown
v/HostAssignAddVariableOp"AssignAddVariableOp_1(1       @9       @A       @I       @a??A??4G?iE??qC????Unknown
V0HostCast"Cast(1       @9       @A       @I       @a??A??4G?i??????Unknown
b1HostDivNoNan"div_no_nan_1(1       @9       @A       @I       @a??A??4G?iE^>?ݎ???Unknown
y2HostReadVariableOp"div_no_nan_1/ReadVariableOp_1(1       @9       @A       @I       @a??A??4G?iŮo&?????Unknown
?3HostBroadcastTo",gradient_tape/mean_squared_error/BroadcastTo(1       @9       @A       @I       @a??A??4G?iE??bx????Unknown
w4HostCast"%gradient_tape/mean_squared_error/Cast(1       @9       @A       @I       @a??A??4G?i?OҞE????Unknown
}5HostMaximum"(gradient_tape/mean_squared_error/Maximum(1       @9       @A       @I       @a??A??4G?iE??????Unknown
u6HostMul"$gradient_tape/mean_squared_error/Mul(1       @9       @A       @I       @a??A??4G?i??4?????Unknown
u7HostSum"$gradient_tape/mean_squared_error/Sum(1       @9       @A       @I       @a??A??4G?iEAfS?????Unknown
u8HostSub"$gradient_tape/mean_squared_error/sub(1       @9       @A       @I       @a??A??4G?iő??z????Unknown
?9HostSquaredDifference"$mean_squared_error/SquaredDifference(1       @9       @A       @I       @a??A??4G?iE???G????Unknown
u:HostSum"$mean_squared_error/weighted_loss/Sum(1       @9       @A       @I       @a??A??4G?i?2?????Unknown
?;HostReadVariableOp"'sequential/Output/MatMul/ReadVariableOp(1       @9       @A       @I       @a??A??4G?iE?+D?????Unknown
T<HostAbs"Abs(1      ??9      ??A      ??I      ??a??A??47?i?+D??????Unknown
t=HostReadVariableOp"Adam/Cast/ReadVariableOp(1      ??9      ??A      ??I      ??a??A??47?i??\??????Unknown
Y>HostPow"Adam/Pow(1      ??9      ??A      ??I      ??a??A??47?i|u?????Unknown
o?HostReadVariableOp"Adam/ReadVariableOp(1      ??9      ??A      ??I      ??a??A??47?iE$??|????Unknown
v@HostAssignAddVariableOp"AssignAddVariableOp_3(1      ??9      ??A      ??I      ??a??A??47?i?̦Zc????Unknown
XAHostCast"Cast_1(1      ??9      ??A      ??I      ??a??A??47?i?t??I????Unknown
aBHostIdentity"Identity(1      ??9      ??A      ??I      ??a??A??47?iؖ0????Unknown?
?CHostDataset"AIterator::Model::ParallelMapV2::Zip[1]::ForeverRepeat::FromTensor(1      ??9      ??A      ??I      ??a??A??47?iE??4????Unknown
VDHostMean"Mean(1      ??9      ??A      ??I      ??a??A??47?i?m	??????Unknown
TEHostMul"Mul(1      ??9      ??A      ??I      ??a??A??47?i?"q?????Unknown
wFHostReadVariableOp"div_no_nan/ReadVariableOp_1(1      ??9      ??A      ??I      ??a??A??47?i?:?????Unknown
wGHostReadVariableOp"div_no_nan_1/ReadVariableOp(1      ??9      ??A      ??I      ??a??A??47?iEfS??????Unknown
HHostFloorDiv")gradient_tape/mean_squared_error/floordiv(1      ??9      ??A      ??I      ??a??A??47?i?lK?????Unknown
wIHostMul"&gradient_tape/mean_squared_error/mul_1(1      ??9      ??A      ??I      ??a??A??47?iŶ??~????Unknown
}JHostRealDiv"(gradient_tape/mean_squared_error/truediv(1      ??9      ??A      ??I      ??a??A??47?i_??e????Unknown
?KHostReadVariableOp",sequential/BrainLayer/BiasAdd/ReadVariableOp(1      ??9      ??A      ??I      ??a??A??47?iE?%L????Unknown
?LHostReadVariableOp"+sequential/BrainLayer/MatMul/ReadVariableOp(1      ??9      ??A      ??I      ??a??A??47?i????2????Unknown
?MHostReadVariableOp"(sequential/Output/BiasAdd/ReadVariableOp(1      ??9      ??A      ??I      ??a??A??47?i?W?a????Unknown
TNHostSub"sub(1      ??9      ??A      ??I      ??a??A??47?i     ???Unknown
HOHostReadVariableOp"div_no_nan/ReadVariableOp(i     ???Unknown
OPHostDivNoNan"&mean_squared_error/weighted_loss/value(i     ???Unknown*?I
?HostResourceApplyAdam""Adam/Adam/update/ResourceApplyAdam(1     ?a@9     ?a@A     ?a@I     ?a@a??????i???????Unknown
uHostFlushSummaryWriter"FlushSummaryWriter(1     ?U@9     ?U@A     ?U@I     ?U@aC?췺?i??;?o????Unknown?
sHostDataset"Iterator::Model::ParallelMapV2(1      R@9      R@A      R@I      R@a#>?Tr^??i?[mM???Unknown
?HostDataset"?Iterator::Model::ParallelMapV2::Zip[0]::FlatMap[0]::Concatenate(1     @S@9     @S@A     ?Q@I     ?Q@a???`???iF|??????Unknown
wHost_FusedMatMul"sequential/BrainLayer/BiasAdd(1     ?G@9     ?G@A     ?G@I     ?G@a<?o?14??i?;?o?1???Unknown
~HostMatMul"*gradient_tape/sequential/BrainLayer/MatMul(1      A@9      A@A      A@I      A@a????O ??i?jch?????Unknown
?HostDataset"5Iterator::Model::ParallelMapV2::Zip[1]::ForeverRepeat(1      ?@9      ?@A      >@I      >@ar^?	???i??t?????Unknown
?HostRandomUniform"<sequential/DropoutLayer/dropout/random_uniform/RandomUniform(1      <@9      <@A      <@I      <@a?H%?e??iR?yY????Unknown
i	HostWriteSummary"WriteSummary(1      5@9      5@A      5@I      5@a??????i???O ????Unknown?
?
HostResourceApplyAdam"$Adam/Adam/update_1/ResourceApplyAdam(1      2@9      2@A      2@I      2@a#>?Tr^??i??,?H???Unknown
^HostGatherV2"GatherV2(1      0@9      0@A      0@I      0@a???,???i-?H%????Unknown
?HostResourceApplyAdam"$Adam/Adam/update_3/ResourceApplyAdam(1      *@9      *@A      *@I      *@aR?yY?'??ix??jch???Unknown
dHostDataset"Iterator::Model(1     @U@9     @U@A      *@I      *@aR?yY?'??i?~???????Unknown
zHostMatMul"&gradient_tape/sequential/Output/MatMul(1      (@9      (@A      (@I      (@a??VCӍ?i????`???Unknown
lHostIteratorGetNext"IteratorGetNext(1      &@9      &@A      &@I      &@ach???V??i[?'?J????Unknown
eHost
LogicalAnd"
LogicalAnd(1      &@9      &@A      &@I      &@ach???V??i??6??;???Unknown?
?HostBiasAddGrad"3gradient_tape/sequential/Output/BiasAdd/BiasAddGrad(1      &@9      &@A      &@I      &@ach???V??i??E|????Unknown
?HostResourceApplyAdam"$Adam/Adam/update_2/ResourceApplyAdam(1      $@9      $@A      $@I      $@aC???ڈ?i??[m???Unknown
?HostBiasAddGrad"7gradient_tape/sequential/BrainLayer/BiasAdd/BiasAddGrad(1      "@9      "@A      "@I      "@a#>?Tr^??i?H%?e???Unknown
|HostMatMul"(gradient_tape/sequential/Output/MatMul_1(1      "@9      "@A      "@I      "@a#>?Tr^??i???`????Unknown
gHostStridedSlice"strided_slice(1      "@9      "@A      "@I      "@a#>?Tr^??i???????Unknown
?HostDynamicStitch".gradient_tape/mean_squared_error/DynamicStitch(1       @9       @A       @I       @a???,???i{??jch???Unknown
sHost_FusedMatMul"sequential/Output/BiasAdd(1       @9       @A       @I       @a???,???iC??????Unknown
[HostAddV2"Adam/add(1      @9      @A      @I      @a?H%?e??ioch??????Unknown
?HostDataset"OIterator::Model::ParallelMapV2::Zip[0]::FlatMap[0]::Concatenate[0]::TensorSlice(1      @9      @A      @I      @a?H%?e??i???VC???Unknown
vHostAssignAddVariableOp"AssignAddVariableOp_2(1      @9      @A      @I      @a??VC?}?i?14??~???Unknown
vHostCast"$sequential/DropoutLayer/dropout/Cast(1      @9      @A      @I      @a??VC?}?i??jch????Unknown
vHostReadVariableOp"Adam/Cast_3/ReadVariableOp(1      @9      @A      @I      @aC????x?i\C?????Unknown
`HostGatherV2"
GatherV2_1(1      @9      @A      @I      @aC????x?iWC????Unknown
?HostTile"5gradient_tape/mean_squared_error/weighted_loss/Tile_1(1      @9      @A      @I      @aC????x?i?????O???Unknown
?HostDivNoNan"?gradient_tape/mean_squared_error/weighted_loss/value/div_no_nan(1      @9      @A      @I      @aC????x?iQ??">????Unknown
? HostCast"2mean_squared_error/weighted_loss/num_elements/Cast(1      @9      @A      @I      @aC????x?i?	???????Unknown
?!HostGreaterEqual",sequential/DropoutLayer/dropout/GreaterEqual(1      @9      @A      @I      @aC????x?i?E|?????Unknown
~"HostAssignAddVariableOp"Adam/Adam/AssignAddVariableOp(1      @9      @A      @I      @a???,?s?i??[m???Unknown
V#HostSum"Sum_2(1      @9      @A      @I      @a???,?s?iC?o?14???Unknown
[$HostPow"
Adam/Pow_1(1      @9      @A      @I      @a??VC?m?iA/??R???Unknown
v%HostAssignAddVariableOp"AssignAddVariableOp_4(1      @9      @A      @I      @a??VC?m?i???;?o???Unknown
?&HostDataset"/Iterator::Model::ParallelMapV2::Zip[0]::FlatMap(1      T@9      T@A      @I      @a??VC?m?i=??~?????Unknown
`'HostDivNoNan"
div_no_nan(1      @9      @A      @I      @a??VC?m?i;4??~????Unknown
i(HostMean"mean_squared_error/Mean(1      @9      @A      @I      @a??VC?m?i9??R????Unknown
t)HostMul"#sequential/DropoutLayer/dropout/Mul(1      @9      @A      @I      @a??VC?m?i7?H%????Unknown
v*HostMul"%sequential/DropoutLayer/dropout/Mul_1(1      @9      @A      @I      @a??VC?m?i59/?????Unknown
]+HostCast"Adam/Cast_1(1       @9       @A       @I       @a???,?c?i???????Unknown
v,HostReadVariableOp"Adam/Cast_2/ReadVariableOp(1       @9       @A       @I       @a???,?c?i????,???Unknown
t-HostAssignAddVariableOp"AssignAddVariableOp(1       @9       @A       @I       @a???,?c?i0?e?@???Unknown
v.HostAssignAddVariableOp"AssignAddVariableOp_1(1       @9       @A       @I       @a???,?c?i??">?T???Unknown
V/HostCast"Cast(1       @9       @A       @I       @a???,?c?i???jch???Unknown
b0HostDivNoNan"div_no_nan_1(1       @9       @A       @I       @a???,?c?i+???E|???Unknown
y1HostReadVariableOp"div_no_nan_1/ReadVariableOp_1(1       @9       @A       @I       @a???,?c?i?yY?'????Unknown
?2HostBroadcastTo",gradient_tape/mean_squared_error/BroadcastTo(1       @9       @A       @I       @a???,?c?i}^?	????Unknown
w3HostCast"%gradient_tape/mean_squared_error/Cast(1       @9       @A       @I       @a???,?c?i&C??????Unknown
}4HostMaximum"(gradient_tape/mean_squared_error/Maximum(1       @9       @A       @I       @a???,?c?i?'?J?????Unknown
u5HostMul"$gradient_tape/mean_squared_error/Mul(1       @9       @A       @I       @a???,?c?ixMw?????Unknown
u6HostSum"$gradient_tape/mean_squared_error/Sum(1       @9       @A       @I       @a???,?c?i!?	??????Unknown
u7HostSub"$gradient_tape/mean_squared_error/sub(1       @9       @A       @I       @a???,?c?i????t???Unknown
?8HostSquaredDifference"$mean_squared_error/SquaredDifference(1       @9       @A       @I       @a???,?c?is???V???Unknown
u9HostSum"$mean_squared_error/weighted_loss/Sum(1       @9       @A       @I       @a???,?c?i?@*9/???Unknown
?:HostReadVariableOp"'sequential/Output/MatMul/ReadVariableOp(1       @9       @A       @I       @a???,?c?iŃ?VC???Unknown
T;HostAbs"Abs(1      ??9      ??A      ??I      ??a???,?S?i?[mM???Unknown
t<HostReadVariableOp"Adam/Cast/ReadVariableOp(1      ??9      ??A      ??I      ??a???,?S?ioh???V???Unknown
Y=HostPow"Adam/Pow(1      ??9      ??A      ??I      ??a???,?S?i????`???Unknown
o>HostReadVariableOp"Adam/ReadVariableOp(1      ??9      ??A      ??I      ??a???,?S?iMw??j???Unknown
v?HostAssignAddVariableOp"AssignAddVariableOp_3(1      ??9      ??A      ??I      ??a???,?S?in????t???Unknown
X@HostCast"Cast_1(1      ??9      ??A      ??I      ??a???,?S?i?14??~???Unknown
aAHostIdentity"Identity(1      ??9      ??A      ??I      ??a???,?S?i????????Unknown?
?BHostDataset"AIterator::Model::ParallelMapV2::Zip[1]::ForeverRepeat::FromTensor(1      ??9      ??A      ??I      ??a???,?S?im?	?????Unknown
VCHostMean"Mean(1      ??9      ??A      ??I      ??a???,?S?iO ?????Unknown
TDHostMul"Mul(1      ??9      ??A      ??I      ??a???,?S?i??6?????Unknown
wEHostReadVariableOp"div_no_nan/ReadVariableOp_1(1      ??9      ??A      ??I      ??a???,?S?ilmMw????Unknown
wFHostReadVariableOp"div_no_nan_1/ReadVariableOp(1      ??9      ??A      ??I      ??a???,?S?i??jch????Unknown
GHostFloorDiv")gradient_tape/mean_squared_error/floordiv(1      ??9      ??A      ??I      ??a???,?S?iR?yY????Unknown
wHHostMul"&gradient_tape/mean_squared_error/mul_1(1      ??9      ??A      ??I      ??a???,?S?ik?'?J????Unknown
}IHostRealDiv"(gradient_tape/mean_squared_error/truediv(1      ??9      ??A      ??I      ??a???,?S?i?6??;????Unknown
?JHostReadVariableOp",sequential/BrainLayer/BiasAdd/ReadVariableOp(1      ??9      ??A      ??I      ??a???,?S?i???,????Unknown
?KHostReadVariableOp"+sequential/BrainLayer/MatMul/ReadVariableOp(1      ??9      ??A      ??I      ??a???,?S?ijC?????Unknown
?LHostReadVariableOp"(sequential/Output/BiasAdd/ReadVariableOp(1      ??9      ??A      ??I      ??a???,?S?i????????Unknown
TMHostSub"sub(1      ??9      ??A      ??I      ??a???,?S?i
     ???Unknown
HNHostReadVariableOp"div_no_nan/ReadVariableOp(i
     ???Unknown
OOHostDivNoNan"&mean_squared_error/weighted_loss/value(i
     ???Unknown2CPU