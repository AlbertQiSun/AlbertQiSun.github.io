---
layout: page
title: projects
permalink: /projects/
description: Code behind my papers, plus agent and systems projects. Everything public is on my <a href="https://github.com/AlbertQiSun">GitHub</a>.
nav: true
nav_order: 2
---

<!-- _pages/projects.md
     Hand-written list instead of the al-folio card grid, so each project gets a short explanation.
     To add a project: copy one entry below. Keep each description to one or two sentences. -->

## research code

**DistOPD** · [code](https://github.com/AlbertQiSun/DistOPD)<br>
Official implementation of _Rethinking Offline On-Policy Distillation_. It covers the full multi-turn agentic search pipeline: a Qwen3-4B student searching a wiki-18 retriever, one-pass teacher scoring with cached top-K probabilities, the distributional distillation loss, and Slurm templates for every stage.

**Search-R1 for Qwen3** · [code](https://github.com/AlbertQiSun/searchr1-for-qwen3)<br>
A rebuild of the Search-R1 agentic RL training pipeline on verl so that it supports Qwen3 models, with BM25 and E5 retrievers and a rule-based answer reward.

**On-policy distillation for search agents** · [code](https://github.com/AlbertQiSun/On-Policy-Distillation-Implementation-for-Search-o1)<br>
On-policy distillation from a Qwen3-32B teacher into small Search-o1 style search agents, with LoRA training and probing scripts and BM25 and E5 retrieval.

## agents and reinforcement learning

**PokeAgent** · [code](https://github.com/AlbertQiSun/PokeAgent)<br>
A Pokémon Showdown battle system (Gen 9 Battle Stadium Singles) where four agents compete: a Gemini agent, a local Qwen3-8B fine-tuned with LoRA SFT on human replays, a PPO agent pretrained by behavioral cloning and then trained through self-play, and a hybrid agent that pairs the PPO policy with LLM reasoning. All four share a battle-intelligence layer for damage calculation, metagame scouting, and opponent tracking.

## systems and community

**NYU Shanghai ICPC training platform**<br>
Together with Prof. Xianbin Gu, I built the training platform for the NYU Shanghai ICPC team (Vue 3, Django). It includes an online judge and LLM-based personalized problem recommendation.