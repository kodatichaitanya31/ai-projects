# Document Q&A

A RAG-style retrieval tool: it splits your text files into paragraphs, ranks them against
your question with TF-IDF, and returns the best matches.

```bash
pip install scikit-learn
python qa.py "What is RAG?"
```

Add your own `.txt` files to `docs/`. To make it a full RAG pipeline, pass the
retrieved paragraphs as context to an LLM (see `../chatbot`).
