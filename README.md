# The-historian
A experiment of toy to using agent to explore the probability of LLMs
Using agent to implement historical research which include information process and summary

> Core principle:
> Anything could be implemented by an agent, should write the agent to do.
> To know the detail. [click here](https://github.com/Archkon/Historian/blob/main/Prototype.md)
# Single agent
## RAG agent
> To act as a RAG-like way to load external knowledge using LLMs
### pre processing 
#### data agent
e.g.
- doc extrator
- data cleaning
- text splitter
- chunck


#### rewrite agent
> semantic search limitation
> limited query perspective
- Q&A (text chunk to qa)
- hyde



#### embedding agent
#### database agent

### post process
#### retrieve agent
> parallel retrieve 
> embedding semantic loss
> core- based  filter
#### rerank agent

## Tools agent
> To act as a agent to choose a kind of tools to observe external world or write codes to implement
### function calling

## memory agent
> To act as memory to manage short-term memory or long-term memory and etc.

> vote and rank to decide importance
### Short-Term Memory agent
> Temporarily stores recent interactions and outcomes
### Long-Term Memory agent
> Preserves valuable insights and learnings from past executions, allowing agents to build and refine their knowledge over time.
### User Memory


**I recognise above three agent as the perception of LLms** 



## Reasoning ability
> This is core ability of the single agent to plan as human
### in-context learning
### zero-shot

### few-shot   
### one-short
### cot
> zero-short CoT    by  “let’s think step by step”  
### least to most
> break down large task into small steps

### self-consistency 
> self-consistency    by more frequency more likely correct   

### ReAct 

### Reflextion

### cot-sc
### tot
## Router agent
> To act as a middle ware to choose which agent should be call
### output agent
### evaluation agent
### Prompt agent
> To act as an agent to using appropriate prompt and refine the prompt
```
##Role
role-play

##instruction
task-solving

##example
method or solution 

##output format
What you need 
```


**action+feedback ⇒external environment**

**A single agent cycle maybe following:**
**perception ⇒ plan ⇒ action ⇒ feedback ⇒reinforce perception**
