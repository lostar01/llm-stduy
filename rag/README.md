###准备环境
```
pip install -qU \
langchain==0.0.316 \
openai==0.28.1 \
tiktoken=0.5.1 \
cohere \
chromadb==0.4.15
```

###RAG 实现的步骤
#### 1.1 文档的加载与切割
```
#安装PDF 解释库
pip install pdfminer.six
```
