# Specifications

## Class Structure

### TradingAlgo

The super-class for all algorithms. Provides all functions needed for writing a trading algo itself.
The implementation overwrites functions that are called from the module execution the algo.

#### Portfolio

Used by the `TradingAlgo` to manage the account attributes like liquidity and open positions

#### Data

Used to interact with all financial data. Manages the API and the storage of the data.

#### Market

The Class the provides access to all functionality related to the marked itself.
This includes all functionality for orders. 

### BackTest

The `Backtest` requires a `TradingAlgo` and all required parameters for back-testing.
It tests the Algo on according to the given parameters and provides ways to read the results.

### WalkForward

Test an algo live on the real market using paper-trading. The constant uptime of the process is implemented by
using a docker.

### Visualizer

The `Visualizer` builds different charts and graphs form data.

## Data Formats

###Time
- Time is represented as epoch time in _ms_
- Time should be accepted as: epoch time, iso, pandas

