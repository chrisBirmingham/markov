# Markov Chain

A python script using Markov chains to generate "readable noncense". Code heavily influenced by Ben Hoyt's [Using a Markov chain to generate readable nonsense with 20 lines of Python](https://benhoyt.com/writings/markov-chain/)
post I found on [Lobst.rs](https://lobste.rs/s/mqhxkp/using_markov_chain_generate_readable) and used to generate my end 
of year review.

## To Build

To build the project run:

```commandline
git clone https://github.com/chrisBirmingham/markov
cd markov
python -m build
```

## Usage

To run the project first create an input file with the text to train the markov script, I chose the Jabberwocky by 
Lewis Carroll. Next run the project like so:

```commandline
python -m markov {input_file.txt}
```

You should get something like this in response

```text
Tumtum tree, And stood awhile in thought. And as in uffish thought he stood, 
The Jabberwock, with eyes of flame, Came whiffling through the tulgey wood, A
nd burbled as it came! One, two! And through and through The vorpal blade wen
t snicker-snack! He left it dead, and with its head He went galumphing back.
```

Have fun.
