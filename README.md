# LLM and processes

### Setup

Create a new conda environment
```bash
conda create -n pyllm python=3.10
conda activate pyllm
```

Install the dependencies
```bash
pip install -r requirements.py
```

Set up OpenAI API key. Create a `.env` file containing this line:
```env
OPENAI_API_KEY=<your key, should start with sk->
```