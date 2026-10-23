# Alice in Wonderland: NLP engine

> Built at **Epitech Rennes** · B-AIA-200 · Artificial Intelligence · March 2026

## Overview

A CLI tool that helps publishers and readers make sense of a book without reading it entirely. It fetches works from **Project Gutenberg**, analyzes them and generates short book cards. Expensive computations are cached so they can be reused.

## Features

- `bookworm.py` CLI with several analysis commands (`--help` lists them)
- Book card generation: `python3 bookworm.py --card 11`
- NLP processing split into modules under `functions/`
- Caching of expensive results

## Tech stack

`Python` · `NLP` · `CLI`

---

## Technical documentation

## Alice in borderland project

[![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)](http://forthebadge.com)

The project is to develop a prototype NLP engine performing operations on books from Project
Gutenberg through dedicated CLI commands.

### To start

- Clone the repository

### Requirements

- Create the environnement by running `python3 -m venv ./venv`
- Activate the environment by running `source ./venv/bin/activate`
- Install dependencies `pip install -r requirements/requirements.txt`

### Help

- To know about all options to run the programm , do : `python3 bookworm.py --help`

### Running

- You only have to run `bookworm.py` with available arguments and parameters. 
- For example : `python3 bookworm.py --card 11` -> It will run the program and you will get the card of the book 11.

---

More of my work on my [portfolio](https://charly-2025.github.io/myPortfolio/).
