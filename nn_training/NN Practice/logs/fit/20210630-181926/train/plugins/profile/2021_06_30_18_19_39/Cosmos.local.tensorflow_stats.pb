"?K
BHostIDLE"IDLE1     \?@A     \?@a???lG??i???lG???Unknown
eHost
LogicalAnd"
LogicalAnd(1      ?@9      ?@A      ?@I      ?@a??*???ibż??G???Unknown?
uHostFlushSummaryWriter"FlushSummaryWriter(1     @T@9     @T@A     @T@I     @T@a=?4?1???i?j&?????Unknown?
sHostDataset"Iterator::Model::ParallelMapV2(1      O@9      O@A      O@I      O@a??c??`??i???{qD???Unknown
?HostDataset"?Iterator::Model::ParallelMapV2::Zip[0]::FlatMap[0]::Concatenate(1     ?O@9     ?O@A      L@I      L@a??ͦW???i$/[?Z????Unknown
?HostResourceApplyAdam""Adam/Adam/update/ResourceApplyAdam(1      J@9      J@A      J@I      J@aU޾?,???i?*??3???Unknown
~HostMatMul"*gradient_tape/sequential/BrainLayer/MatMul(1      B@9      B@A      B@I      B@a?G???i,;???B???Unknown
?HostDataset"5Iterator::Model::ParallelMapV2::Zip[1]::ForeverRepeat(1     ?B@9     ?B@A      @@I      @@aA??P?B|?i:?N{???Unknown
w	Host_FusedMatMul"sequential/BrainLayer/BiasAdd(1      <@9      <@A      <@I      <@a??ͦW?x?i???ì???Unknown
?
HostRandomUniform"<sequential/DropoutLayer/dropout/random_uniform/RandomUniform(1      6@9      6@A      6@I      6@a??'?ms?i??K?????Unknown
?HostResourceApplyAdam"$Adam/Adam/update_3/ResourceApplyAdam(1      4@9      4@A      4@I      4@ahҒR??q?i?|??????Unknown
iHostWriteSummary"WriteSummary(1      4@9      4@A      4@I      4@ahҒR??q?ig:!?E???Unknown?
?HostResourceApplyAdam"$Adam/Adam/update_2/ResourceApplyAdam(1      2@9      2@A      2@I      2@a?G??o?i?B :???Unknown
?HostResourceApplyAdam"$Adam/Adam/update_1/ResourceApplyAdam(1      .@9      .@A      .@I      .@a?;?{?~j?i????T???Unknown
^HostGatherV2"GatherV2(1      .@9      .@A      .@I      .@a?;?{?~j?i'?o???Unknown
zHostMatMul"&gradient_tape/sequential/Output/MatMul(1      (@9      (@A      (@I      (@a?/??2e?iW?@????Unknown
[HostAddV2"Adam/add(1      "@9      "@A      "@I      "@a?G??_?i{/??%????Unknown
dHostDataset"Iterator::Model(1     ?Q@9     ?Q@A      "@I      "@a?G??_?i??
????Unknown
gHostStridedSlice"strided_slice(1      "@9      "@A      "@I      "@a?G??_?i?7???????Unknown
lHostIteratorGetNext"IteratorGetNext(1       @9       @A       @I       @aA??P?B\?i8?1?????Unknown
?HostDynamicStitch".gradient_tape/mean_squared_error/DynamicStitch(1       @9       @A       @I       @aA??P?B\?i?"?83????Unknown
`HostGatherV2"
GatherV2_1(1      @9      @A      @I      @a??ͦW?X?is??d?????Unknown
xHostDataset"#Iterator::Model::ParallelMapV2::Zip(1     ?[@9     ?[@A      @I      @a??ͦW?X?i9????????Unknown
?HostDataset"OIterator::Model::ParallelMapV2::Zip[0]::FlatMap[0]::Concatenate[0]::TensorSlice(1      @9      @A      @I      @a??ͦW?X?i?VT?J????Unknown
sHost_FusedMatMul"sequential/Output/BiasAdd(1      @9      @A      @I      @a??ͦW?X?iŽ'?????Unknown
?HostBiasAddGrad"3gradient_tape/sequential/Output/BiasAdd/BiasAddGrad(1      @9      @A      @I      @a?/??2U?i?&?@???Unknown
|HostMatMul"(gradient_tape/sequential/Output/MatMul_1(1      @9      @A      @I      @a?/??2U?i?m$?????Unknown
YHostPow"Adam/Pow(1      @9      @A      @I      @ahҒR??Q?i^?M?????Unknown
tHostAssignAddVariableOp"AssignAddVariableOp(1      @9      @A      @I      @ahҒR??Q?i? w??(???Unknown
?HostDataset"AIterator::Model::ParallelMapV2::Zip[1]::ForeverRepeat::FromTensor(1      @9      @A      @I      @ahҒR??Q?i0J?lX1???Unknown
?HostBiasAddGrad"7gradient_tape/sequential/BrainLayer/BiasAdd/BiasAddGrad(1      @9      @A      @I      @ahҒR??Q?i???B-:???Unknown
u HostSum"$mean_squared_error/weighted_loss/Sum(1      @9      @A      @I      @ahҒR??Q?i??C???Unknown
?!HostReadVariableOp"+sequential/BrainLayer/MatMul/ReadVariableOp(1      @9      @A      @I      @ahҒR??Q?ik&??K???Unknown
?"HostTile"5gradient_tape/mean_squared_error/weighted_loss/Tile_1(1      @9      @A      @I      @aA??P?BL?i&ap??R???Unknown
?#HostGreaterEqual",sequential/DropoutLayer/dropout/GreaterEqual(1      @9      @A      @I      @aA??P?BL?i???E?Y???Unknown
?$HostReadVariableOp"'sequential/Output/MatMul/ReadVariableOp(1      @9      @A      @I      @aA??P?BL?i???a???Unknown
T%HostSub"sub(1      @9      @A      @I      @aA??P?BL?iWm?h???Unknown
]&HostCast"Adam/Cast_1(1      @9      @A      @I      @a?/??2E?ic=?fm???Unknown
o'HostReadVariableOp"Adam/ReadVariableOp(1      @9      @A      @I      @a?/??2E?ioik??r???Unknown
v(HostAssignAddVariableOp"AssignAddVariableOp_2(1      @9      @A      @I      @a?/??2E?i{???w???Unknown
v)HostAssignAddVariableOp"AssignAddVariableOp_3(1      @9      @A      @I      @a?/??2E?i??i?K}???Unknown
V*HostCast"Cast(1      @9      @A      @I      @a?/??2E?i????????Unknown
?+HostDataset"/Iterator::Model::ParallelMapV2::Zip[0]::FlatMap(1     ?P@9     ?P@A      @I      @a?/??2E?i?h??????Unknown
V,HostSum"Sum_2(1      @9      @A      @I      @a?/??2E?i?E?1????Unknown
u-HostSub"$gradient_tape/mean_squared_error/sub(1      @9      @A      @I      @a?/??2E?i?qf?}????Unknown
?.HostDivNoNan"?gradient_tape/mean_squared_error/weighted_loss/value/div_no_nan(1      @9      @A      @I      @a?/??2E?iÝ? ʗ???Unknown
i/HostMean"mean_squared_error/Mean(1      @9      @A      @I      @a?/??2E?i??d?????Unknown
?0HostSquaredDifference"$mean_squared_error/SquaredDifference(1      @9      @A      @I      @a?/??2E?i???!c????Unknown
T1HostAbs"Abs(1       @9       @A       @I       @aA??P?B<?i8?w?????Unknown
~2HostAssignAddVariableOp"Adam/Adam/AssignAddVariableOp(1       @9       @A       @I       @aA??P?B<?i?08?s????Unknown
v3HostReadVariableOp"Adam/Cast_2/ReadVariableOp(1       @9       @A       @I       @aA??P?B<?i?M?"?????Unknown
v4HostReadVariableOp"Adam/Cast_3/ReadVariableOp(1       @9       @A       @I       @aA??P?B<?iOk?x?????Unknown
[5HostPow"
Adam/Pow_1(1       @9       @A       @I       @aA??P?B<?i??6?????Unknown
v6HostAssignAddVariableOp"AssignAddVariableOp_1(1       @9       @A       @I       @aA??P?B<?i	??#?????Unknown
v7HostAssignAddVariableOp"AssignAddVariableOp_4(1       @9       @A       @I       @aA??P?B<?ifÊy????Unknown
X8HostCast"Cast_1(1       @9       @A       @I       @aA??P?B<?i??4ϥ????Unknown
V9HostMean"Mean(1       @9       @A       @I       @aA??P?B<?i ??$.????Unknown
b:HostDivNoNan"div_no_nan_1(1       @9       @A       @I       @aA??P?B<?i}?z?????Unknown
};HostMaximum"(gradient_tape/mean_squared_error/Maximum(1       @9       @A       @I       @aA??P?B<?i?83?>????Unknown
u<HostMul"$gradient_tape/mean_squared_error/Mul(1       @9       @A       @I       @aA??P?B<?i7V?%?????Unknown
u=HostSum"$gradient_tape/mean_squared_error/Sum(1       @9       @A       @I       @aA??P?B<?i?s?{O????Unknown
w>HostMul"&gradient_tape/mean_squared_error/mul_1(1       @9       @A       @I       @aA??P?B<?i??1??????Unknown
}?HostRealDiv"(gradient_tape/mean_squared_error/truediv(1       @9       @A       @I       @aA??P?B<?iN??&`????Unknown
?@HostCast"2mean_squared_error/weighted_loss/num_elements/Cast(1       @9       @A       @I       @aA??P?B<?i?˅|?????Unknown
?AHostReadVariableOp",sequential/BrainLayer/BiasAdd/ReadVariableOp(1       @9       @A       @I       @aA??P?B<?i?/?p????Unknown
vBHostCast"$sequential/DropoutLayer/dropout/Cast(1       @9       @A       @I       @aA??P?B<?ie?'?????Unknown
tCHostMul"#sequential/DropoutLayer/dropout/Mul(1       @9       @A       @I       @aA??P?B<?i?#?}?????Unknown
vDHostMul"%sequential/DropoutLayer/dropout/Mul_1(1       @9       @A       @I       @aA??P?B<?iA.?	????Unknown
tEHostReadVariableOp"Adam/Cast/ReadVariableOp(1      ??9      ??A      ??I      ??aA??P?B,?i?O??????Unknown
aFHostIdentity"Identity(1      ??9      ??A      ??I      ??aA??P?B,?i}^?(?????Unknown?
TGHostMul"Mul(1      ??9      ??A      ??I      ??aA??P?B,?i,m?SV????Unknown
`HHostDivNoNan"
div_no_nan(1      ??9      ??A      ??I      ??aA??P?B,?i?{?~????Unknown
uIHostReadVariableOp"div_no_nan/ReadVariableOp(1      ??9      ??A      ??I      ??aA??P?B,?i??W??????Unknown
wJHostReadVariableOp"div_no_nan/ReadVariableOp_1(1      ??9      ??A      ??I      ??aA??P?B,?i9?,Ԣ????Unknown
wKHostReadVariableOp"div_no_nan_1/ReadVariableOp(1      ??9      ??A      ??I      ??aA??P?B,?i???f????Unknown
yLHostReadVariableOp"div_no_nan_1/ReadVariableOp_1(1      ??9      ??A      ??I      ??aA??P?B,?i???)+????Unknown
?MHostBroadcastTo",gradient_tape/mean_squared_error/BroadcastTo(1      ??9      ??A      ??I      ??aA??P?B,?iFūT?????Unknown
wNHostCast"%gradient_tape/mean_squared_error/Cast(1      ??9      ??A      ??I      ??aA??P?B,?i?Ӏ?????Unknown
OHostFloorDiv")gradient_tape/mean_squared_error/floordiv(1      ??9      ??A      ??I      ??aA??P?B,?i??U?w????Unknown
|PHostDivNoNan"&mean_squared_error/weighted_loss/value(1      ??9      ??A      ??I      ??aA??P?B,?iS?*?;????Unknown
?QHostReadVariableOp"(sequential/Output/BiasAdd/ReadVariableOp(1      ??9      ??A      ??I      ??aA??P?B,?i     ???Unknown*?J
eHost
LogicalAnd"
LogicalAnd(1      ?@9      ?@A      ?@I      ?@a?Z܄?]??i?Z܄?]???Unknown?
uHostFlushSummaryWriter"FlushSummaryWriter(1     @T@9     @T@A     @T@I     @T@a?@T:?g??ix??	?????Unknown?
sHostDataset"Iterator::Model::ParallelMapV2(1      O@9      O@A      O@I      O@a:?g *??i?0???M???Unknown
?HostDataset"?Iterator::Model::ParallelMapV2::Zip[0]::FlatMap[0]::Concatenate(1     ?O@9     ?O@A      L@I      L@a^-n?????ir?w?????Unknown
?HostResourceApplyAdam""Adam/Adam/update/ResourceApplyAdam(1      J@9      J@A      J@I      J@a *?3??i?w??	???Unknown
~HostMatMul"*gradient_tape/sequential/BrainLayer/MatMul(1      B@9      B@A      B@I      B@aT:?g *??i?w??	????Unknown
?HostDataset"5Iterator::Model::ParallelMapV2::Zip[1]::ForeverRepeat(1     ?B@9     ?B@A      @@I      @@a?3?????i??]-n????Unknown
wHost_FusedMatMul"sequential/BrainLayer/BiasAdd(1      <@9      <@A      <@I      <@a^-n?????i?jq?w???Unknown
?	HostRandomUniform"<sequential/DropoutLayer/dropout/random_uniform/RandomUniform(1      6@9      6@A      6@I      6@a?#{?ґ?iD?#{???Unknown
?
HostResourceApplyAdam"$Adam/Adam/update_3/ResourceApplyAdam(1      4@9      4@A      4@I      4@ah *?3??i???????Unknown
iHostWriteSummary"WriteSummary(1      4@9      4@A      4@I      4@ah *?3??i?w??	???Unknown?
?HostResourceApplyAdam"$Adam/Adam/update_2/ResourceApplyAdam(1      2@9      2@A      2@I      2@aT:?g *??i??7a~???Unknown
?HostResourceApplyAdam"$Adam/Adam/update_1/ResourceApplyAdam(1      .@9      .@A      .@I      .@a?0???M??i???M?????Unknown
^HostGatherV2"GatherV2(1      .@9      .@A      .@I      .@a?0???M??i??td?@???Unknown
zHostMatMul"&gradient_tape/sequential/Output/MatMul(1      (@9      (@A      (@I      (@a?&??jq??i?3?????Unknown
[HostAddV2"Adam/add(1      "@9      "@A      "@I      "@aT:?g *}?i?=Q?????Unknown
dHostDataset"Iterator::Model(1     ?Q@9     ?Q@A      "@I      "@aT:?g *}?i?ґ=???Unknown
gHostStridedSlice"strided_slice(1      "@9      "@A      "@I      "@aT:?g *}?i|?ґ=???Unknown
lHostIteratorGetNext"IteratorGetNext(1       @9       @A       @I       @a?3???y?i?&??jq???Unknown
?HostDynamicStitch".gradient_tape/mean_squared_error/DynamicStitch(1       @9       @A       @I       @a?3???y?iLG?D????Unknown
`HostGatherV2"
GatherV2_1(1      @9      @A      @I      @a^-n???v?i?#{?????Unknown
xHostDataset"#Iterator::Model::ParallelMapV2::Zip(1     ?[@9     ?[@A      @I      @a^-n???v?i     ???Unknown
?HostDataset"OIterator::Model::ParallelMapV2::Zip[0]::FlatMap[0]::Concatenate[0]::TensorSlice(1      @9      @A      @I      @a^-n???v?i]܄?]-???Unknown
sHost_FusedMatMul"sequential/Output/BiasAdd(1      @9      @A      @I      @a^-n???v?i??	??Z???Unknown
?HostBiasAddGrad"3gradient_tape/sequential/Output/BiasAdd/BiasAddGrad(1      @9      @A      @I      @a?&??jqs?iQ?Ȟ????Unknown
|HostMatMul"(gradient_tape/sequential/Output/MatMul_1(1      @9      @A      @I      @a?&??jqs?iT?Ȟ?????Unknown
YHostPow"Adam/Pow(1      @9      @A      @I      @ah *?3p?i?=Q?????Unknown
tHostAssignAddVariableOp"AssignAddVariableOp(1      @9      @A      @I      @ah *?3p?i֑=Q????Unknown
?HostDataset"AIterator::Model::ParallelMapV2::Zip[1]::ForeverRepeat::FromTensor(1      @9      @A      @I      @ah *?3p?i?w??	???Unknown
?HostBiasAddGrad"7gradient_tape/sequential/BrainLayer/BiasAdd/BiasAddGrad(1      @9      @A      @I      @ah *?3p?iX:?g *???Unknown
uHostSum"$mean_squared_error/weighted_loss/Sum(1      @9      @A      @I      @ah *?3p?i????J???Unknown
? HostReadVariableOp"+sequential/BrainLayer/MatMul/ReadVariableOp(1      @9      @A      @I      @ah *?3p?i??&??j???Unknown
?!HostTile"5gradient_tape/mean_squared_error/weighted_loss/Tile_1(1      @9      @A      @I      @a?3???i?i??Z܄???Unknown
?"HostGreaterEqual",sequential/DropoutLayer/dropout/GreaterEqual(1      @9      @A      @I      @a?3???i?iBQ?Ȟ???Unknown
?#HostReadVariableOp"'sequential/Output/MatMul/ReadVariableOp(1      @9      @A      @I      @a?3???i?iv?w?????Unknown
T$HostSub"sub(1      @9      @A      @I      @a?3???i?i?#{?????Unknown
]%HostCast"Adam/Cast_1(1      @9      @A      @I      @a?&??jqc?i??jq????Unknown
o&HostReadVariableOp"Adam/ReadVariableOp(1      @9      @A      @I      @a?&??jqc?i??Z܄????Unknown
v'HostAssignAddVariableOp"AssignAddVariableOp_2(1      @9      @A      @I      @a?&??jqc?i?JG????Unknown
v(HostAssignAddVariableOp"AssignAddVariableOp_3(1      @9      @A      @I      @a?&??jqc?iFT:?g ???Unknown
V)HostCast"Cast(1      @9      @A      @I      @a?&??jqc?im *?3???Unknown
?*HostDataset"/Iterator::Model::ParallelMapV2::Zip[0]::FlatMap(1     ?P@9     ?P@A      @I      @a?&??jqc?i???JG???Unknown
V+HostSum"Sum_2(1      @9      @A      @I      @a?&??jqc?i??	??Z???Unknown
u,HostSub"$gradient_tape/mean_squared_error/sub(1      @9      @A      @I      @a?&??jqc?i???]-n???Unknown
?-HostDivNoNan"?gradient_tape/mean_squared_error/weighted_loss/value/div_no_nan(1      @9      @A      @I      @a?&??jqc?i	Q?Ȟ????Unknown
i.HostMean"mean_squared_error/Mean(1      @9      @A      @I      @a?&??jqc?i0?3????Unknown
?/HostSquaredDifference"$mean_squared_error/SquaredDifference(1      @9      @A      @I      @a?&??jqc?iW?Ȟ?????Unknown
T0HostAbs"Abs(1       @9       @A       @I       @a?3???Y?iqq?w????Unknown
~1HostAssignAddVariableOp"Adam/Adam/AssignAddVariableOp(1       @9       @A       @I       @a?3???Y?i??]-n????Unknown
v2HostReadVariableOp"Adam/Cast_2/ReadVariableOp(1       @9       @A       @I       @a?3???Y?i???td????Unknown
v3HostReadVariableOp"Adam/Cast_3/ReadVariableOp(1       @9       @A       @I       @a?3???Y?i?	??Z????Unknown
[4HostPow"
Adam/Pow_1(1       @9       @A       @I       @a?3???Y?iّ=Q????Unknown
v5HostAssignAddVariableOp"AssignAddVariableOp_1(1       @9       @A       @I       @a?3???Y?i??JG????Unknown
v6HostAssignAddVariableOp"AssignAddVariableOp_4(1       @9       @A       @I       @a?3???Y?i?ґ=???Unknown
X7HostCast"Cast_1(1       @9       @A       @I       @a?3???Y?i'*?3???Unknown
V8HostMean"Mean(1       @9       @A       @I       @a?3???Y?iA?g *???Unknown
b9HostDivNoNan"div_no_nan_1(1       @9       @A       @I       @a?3???Y?i[:?g *???Unknown
}:HostMaximum"(gradient_tape/mean_squared_error/Maximum(1       @9       @A       @I       @a?3???Y?iu???7???Unknown
u;HostMul"$gradient_tape/mean_squared_error/Mul(1       @9       @A       @I       @a?3???Y?i?JG?D???Unknown
u<HostSum"$gradient_tape/mean_squared_error/Sum(1       @9       @A       @I       @a?3???Y?i?ґ=Q???Unknown
w=HostMul"&gradient_tape/mean_squared_error/mul_1(1       @9       @A       @I       @a?3???Y?i?Z܄?]???Unknown
}>HostRealDiv"(gradient_tape/mean_squared_error/truediv(1       @9       @A       @I       @a?3???Y?i??&??j???Unknown
??HostCast"2mean_squared_error/weighted_loss/num_elements/Cast(1       @9       @A       @I       @a?3???Y?i?jq?w???Unknown
?@HostReadVariableOp",sequential/BrainLayer/BiasAdd/ReadVariableOp(1       @9       @A       @I       @a?3???Y?i??Z܄???Unknown
vAHostCast"$sequential/DropoutLayer/dropout/Cast(1       @9       @A       @I       @a?3???Y?i+{?ґ???Unknown
tBHostMul"#sequential/DropoutLayer/dropout/Mul(1       @9       @A       @I       @a?3???Y?iEQ?Ȟ???Unknown
vCHostMul"%sequential/DropoutLayer/dropout/Mul_1(1       @9       @A       @I       @a?3???Y?i_??0?????Unknown
tDHostReadVariableOp"Adam/Cast/ReadVariableOp(1      ??9      ??A      ??I      ??a?3???I?il?@T:????Unknown
aEHostIdentity"Identity(1      ??9      ??A      ??I      ??a?3???I?iy?w?????Unknown?
TFHostMul"Mul(1      ??9      ??A      ??I      ??a?3???I?i?W??0????Unknown
`GHostDivNoNan"
div_no_nan(1      ??9      ??A      ??I      ??a?3???I?i??0??????Unknown
uHHostReadVariableOp"div_no_nan/ReadVariableOp(1      ??9      ??A      ??I      ??a?3???I?i????&????Unknown
wIHostReadVariableOp"div_no_nan/ReadVariableOp_1(1      ??9      ??A      ??I      ??a?3???I?i?#{?????Unknown
wJHostReadVariableOp"div_no_nan_1/ReadVariableOp(1      ??9      ??A      ??I      ??a?3???I?i?g *????Unknown
yKHostReadVariableOp"div_no_nan_1/ReadVariableOp_1(1      ??9      ??A      ??I      ??a?3???I?iǫ?M?????Unknown
?LHostBroadcastTo",gradient_tape/mean_squared_error/BroadcastTo(1      ??9      ??A      ??I      ??a?3???I?i??jq????Unknown
wMHostCast"%gradient_tape/mean_squared_error/Cast(1      ??9      ??A      ??I      ??a?3???I?i?3??????Unknown
NHostFloorDiv")gradient_tape/mean_squared_error/floordiv(1      ??9      ??A      ??I      ??a?3???I?i?w??	????Unknown
|OHostDivNoNan"&mean_squared_error/weighted_loss/value(1      ??9      ??A      ??I      ??a?3???I?i??Z܄????Unknown
?PHostReadVariableOp"(sequential/Output/BiasAdd/ReadVariableOp(1      ??9      ??A      ??I      ??a?3???I?i     ???Unknown2CPU