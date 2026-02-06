# Floor Plan Chair Counter

A command-line tool that reads apartment floor plans from text files and counts different types of chairs (W, P, S, C) per room.

> **Note:** See the tool in action under GitHub Actions CI/CD pipeline. No need to run/check localy.

## Installation

```bash
make install-uv  # install uv package manager
make setup        # install dependencies
```

## Usage

```bash
uv run python main.py <floor_plan.txt>
```

## Solution

The floor plan is parsed into a 2D NumPy character array. Walls (`+`, `-`, `|`, `/`) are identified and a boolean walkable mask is created.

Room names are extracted using regex to find `(name)` patterns. Connected regions are labeled with `scipy.ndimage.label`. Each room's region is identified by the label at its name position, then chairs are counted per region.

**Note:** To demonstrate understanding of the underlying algorithm and avoid over-reliance on image processing libraries, a custom BFS flood fill implementation (`label_rooms`) is also included as an alternative to scipy's labeling.

## Instruction


Apartment And Chair Delivery Limited has a unique position on the housing market. The company not only builds apartments, but also equips them with chairs.
Now the business has grown continuously over the past few years and there are a few organizational problems that could be solved by automation.
We will focus on one of them here:

While a new residential building is erected, the chairs that are to be placed there need to be produced. In order to be able to plan this, the home buyers indicate the desired position of the armchairs in their home on a floor plan at the time of purchase. These plans are collected, and the number of different chairs to be produced are counted from them. The plans are also used to steer the workers carrying the chairs into the building when furnishing the apartments.

In the recent past, when manually counting the various types of chairs in the floor plans, many mistakes were made and caused great resentment among customers. That is why the owner of the company asked us to automate this process.

Unfortunately, the plans are in a very old format (the company's systems are still from the eighties), so modern planning software cannot be used here. An example of such an apartment plan is attached.

We now need a command line tool that reads in such a file and outputs the following information:
- Number of different chair types for the apartment
- Number of different chair types per room

The different types of chairs are as follows:
W: wooden chair
P: plastic chair
S: sofa chair
C: china chair

The output must look exactly like this so that it can be read in with the old system:

```
total:
W: 3, P: 2, S: 0, C: 0
living room:
W: 3, P: 0, S: 0, C: 0
office:
W: 0, P: 2, S: 0, C: 0
```

The names of the rooms must be sorted alphabetically in the output.

Our sales team has promised Apartment And Chair Delivery Limited a solution within 5 days from now. I know that is very ambitious, but as you are our best developer, we all count on you.
