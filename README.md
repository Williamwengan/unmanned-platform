下载 ollama 
https://github.com/ollama/ollama/releases

解压
tar --use-compress-program=unzstd -xvf filename.tar.zst -C /path/to/destination/

cd bin
export PATH=$PATH:/data1/wenganye/project/qwen/bin

./ollama serve

新开窗口 
./ollama run qwen3-vl:8b
