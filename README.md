# Algo Strategy Tester

This application lets you run three pre-defined algorithmic trading strategies on stock data you select. Results are displayed in an interactive graph that you can use to inspect the results. Resulting data and still images of the graphs may be saved if wanted. Enjoy!

## Project Goals and Objectives:

- Learn about successful Trend Trading methodologies
- Research and use new APIs for accessing data plotting data
- Implement an application framework in Python to simulate the results of our trading algorithms
- Test our application against various stock data to determine how our algorithms perform historically against the overall market or specific stocks
- Finally, create the basic structure for what an algorithmic trading application could look like

---

## Strategies Used for Testing:

We implemented the following three algorithmic trading strategies:

### Donchian's 4 Week Rule 

![Donchian](https://user-images.githubusercontent.com/105619339/180354817-8f77e71b-7196-452e-8415-ec411196089d.png)

### Dreyfus' 52 Week Rule

![Dreyfus](https://user-images.githubusercontent.com/105619339/180354826-7c7a9ad9-cdbf-4c1f-933f-b71c39b8c00f.png)

### 20v200 SMA Golden Cross 

![Golden Cross](https://user-images.githubusercontent.com/105619339/180354831-1f51f710-d167-4ed9-8317-f22083befcc0.png)

---

## Technologies

The following libraries / tools are required our code
```text
- anaconda
- python 3.7
- pandas-datareader=0.10.0
- plotly==5.9.0
- kaleido==0.2.1
- questionary==1.10.0
- requests==2.28.1
```

Please create a conda environment using Python 3.7 (ex: "`conda create -n algo python=3.7`")

---

## Installation Guide

You have a few options to install this application on your computer, two popular options are:
1. Download a ZIP of this repositories files [here](https://github.com/warp-9000/algo-trader/archive/refs/heads/main.zip).
2. [Fork this public respository](https://docs.github.com/en/get-started/quickstart/fork-a-repo "Fork a Repo - GitHub Docs") to your github account.

After forking this repository you can...
1. Download a ZIP of your repositories files, or
2. Use "`git clone your-username@domain.com:your-git-username/algo-trader.git`" to download a copy of the forked respository to your computer.

Forking has the added benefit of easily allowing you to keep your application files up-to-date should any changes or improvements be made in the future.

---

## Usage

***Please note:*** *these usage instructions assume you have installed Python 3.7 and setup an environment where the libraries and frameworks listed in [Technologies](##Technologies) are installed.*

1. Navigate to the root folder of your repository.
2. Run the application by typing "`python app.py`" and pressing *ENTER*.
3. Respond to the prompts as shown.

An example of the application running:
<p align="center">
    <img src="https://github.com/warp-9000/algo-trader/blob/main/images/algo-trader-app-usage.gif?raw=true" alt="python app.py in terminal" width="55%"/>
</p>

---

## Contributors

Thanks!

<a href="https://github.com/Warp-9000/algo-trader/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=warp-9000/algo-trader" />
</a>

---

## License

This project is currently licensed under GNU GPLv3. Please see the LICENSE file [here](https://github.com/warp-9000/algo-trader/blob/main/LICENSE).