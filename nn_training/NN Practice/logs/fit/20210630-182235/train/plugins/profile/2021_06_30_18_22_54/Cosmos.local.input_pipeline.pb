	D?l?????D?l?????!D?l?????	?L5a(@?L5a(@!?L5a(@"{
=type.googleapis.com/tensorflow.profiler.PerGenericStepDetails:D?l?????#??~j???Aw??/???Y!?rh????rEagerKernelExecute 0*	     ?h@2U
Iterator::Model::ParallelMapV2;?O??n??!?S?r
^B@);?O??n??1?S?r
^B@:Preprocessing2v
?Iterator::Model::ParallelMapV2::Zip[0]::FlatMap[0]::Concatenate??ʡE???!I?$I??C@)?Q?????1?m۶m?A@:Preprocessing2l
5Iterator::Model::ParallelMapV2::Zip[1]::ForeverRepeatX9??v???!i????/@)???Q???1?????.@:Preprocessing2F
Iterator::Model??(\?µ?!?)x9?E@)9??v????1??>4և@:Preprocessing2?
OIterator::Model::ParallelMapV2::Zip[0]::FlatMap[0]::Concatenate[0]::TensorSlicey?&1?|?!$I?$I?@)y?&1?|?1$I?$I?@:Preprocessing2f
/Iterator::Model::ParallelMapV2::Zip[0]::FlatMap{?G?z??!?Cc}hD@)?~j?t?h?1?Cc}??:Preprocessing2x
AIterator::Model::ParallelMapV2::Zip[1]::ForeverRepeat::FromTensor????MbP?!????S??)????MbP?1????S??:Preprocessing:?
]Enqueuing data: you may want to combine small input data chunks into fewer but larger chunks.
?Data preprocessing: you may increase num_parallel_calls in <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#map" target="_blank">Dataset map()</a> or preprocess the data OFFLINE.
?Reading data from files in advance: you may tune parameters in the following tf.data API (<a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#prefetch" target="_blank">prefetch size</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#interleave" target="_blank">interleave cycle_length</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/TFRecordDataset#class_tfrecorddataset" target="_blank">reader buffer_size</a>)
?Reading data from files on demand: you should read data IN ADVANCE using the following tf.data API (<a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#prefetch" target="_blank">prefetch</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#interleave" target="_blank">interleave</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/TFRecordDataset#class_tfrecorddataset" target="_blank">reader buffer</a>)
?Other data reading or processing: you may consider using the <a href="https://www.tensorflow.org/programmers_guide/datasets" target="_blank">tf.data API</a> (if you are not using it now)?
:type.googleapis.com/tensorflow.profiler.BottleneckAnalysis?
both?Your program is MODERATELY input-bound because 12.2% of the total step time sampled is waiting for input. Therefore, you would need to reduce both the input time and other time.no*high2t17.5 % of the total step time sampled is spent on 'All Others' time. This could be due to Python execution overhead.9?L5a(@I?pV??U@Zno>Look at Section 3 for the breakdown of input time on the host.B?
@type.googleapis.com/tensorflow.profiler.GenericStepTimeBreakdown?
	#??~j???#??~j???!#??~j???      ??!       "      ??!       *      ??!       2	w??/???w??/???!w??/???:      ??!       B      ??!       J	!?rh????!?rh????!!?rh????R      ??!       Z	!?rh????!?rh????!!?rh????b      ??!       JCPU_ONLYY?L5a(@b q?pV??U@