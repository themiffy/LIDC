	X9�H��@X9�H��@!X9�H��@	�Wb�9ӂ?�Wb�9ӂ?!�Wb�9ӂ?"e
=type.googleapis.com/tensorflow.profiler.PerGenericStepDetails$X9�H��@���K7�?A��(\��@Y��C�l�?*	     �g@2U
Iterator::Model::ParallelMapV2㥛� ��?!�)_�%C@)㥛� ��?1�)_�%C@:Preprocessing2v
?Iterator::Model::ParallelMapV2::Zip[0]::FlatMap[2]::Concatenate�������?!�* �-:@)j�t��?1�l�Y�6@:Preprocessing2Z
#Iterator::Model::ParallelMapV2::Zip���Mb�?!
G��y�H@)ˡE����?1U��Iw5@:Preprocessing2x
AIterator::Model::ParallelMapV2::Zip[1]::ForeverRepeat::FromTensor9��v���?! �-�9@)9��v���?1 �-�9@:Preprocessing2F
Iterator::Model/�$��?!�uX�Q�E@)�I+��?1/c��a	@:Preprocessing2�
OIterator::Model::ParallelMapV2::Zip[0]::FlatMap[2]::Concatenate[0]::TensorSlicey�&1�|?!��uX�Q@)y�&1�|?1��uX�Q@:Preprocessing2f
/Iterator::Model::ParallelMapV2::Zip[0]::FlatMap�A`��"�?!�K8��;@)�~j�t�h?1�=��!�?:Preprocessing:�
]Enqueuing data: you may want to combine small input data chunks into fewer but larger chunks.
�Data preprocessing: you may increase num_parallel_calls in <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#map" target="_blank">Dataset map()</a> or preprocess the data OFFLINE.
�Reading data from files in advance: you may tune parameters in the following tf.data API (<a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#prefetch" target="_blank">prefetch size</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#interleave" target="_blank">interleave cycle_length</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/TFRecordDataset#class_tfrecorddataset" target="_blank">reader buffer_size</a>)
�Reading data from files on demand: you should read data IN ADVANCE using the following tf.data API (<a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#prefetch" target="_blank">prefetch</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#interleave" target="_blank">interleave</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/TFRecordDataset#class_tfrecorddataset" target="_blank">reader buffer</a>)
�Other data reading or processing: you may consider using the <a href="https://www.tensorflow.org/programmers_guide/datasets" target="_blank">tf.data API</a> (if you are not using it now)�
:type.googleapis.com/tensorflow.profiler.BottleneckAnalysis�
device�Your program is NOT input-bound because only 0.0% of the total step time sampled is waiting for input. Therefore, you should focus on reducing other time.no*no9�Wb�9ӂ?I�|1fi�X@Zno#You may skip the rest of this page.B�
@type.googleapis.com/tensorflow.profiler.GenericStepTimeBreakdown�
	���K7�?���K7�?!���K7�?      ��!       "      ��!       *      ��!       2	��(\��@��(\��@!��(\��@:      ��!       B      ��!       J	��C�l�?��C�l�?!��C�l�?R      ��!       Z	��C�l�?��C�l�?!��C�l�?b      ��!       JCPU_ONLYY�Wb�9ӂ?b q�|1fi�X@