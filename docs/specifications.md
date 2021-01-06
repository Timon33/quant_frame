# Specifications

## Classes

### TradingAlgo

The super-class for all algorithms. Provides all functions needed for writing a trading algo itself.
The implementation overwrites functions that are called from the module execution the algo.

#### Portfolio

Used by the `TradingAlgo` to manage the account attributes like liquidity and open positions

#### Data

Used to interact with all financial data. Manages the API and the storage of the data.

#### Broker

The Class the provides access to all functionality related to the exchange.
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

- Time is stored as `datetime.datetime` and `datetime.timedelta` internally

### Symbols

- the `quant_frame.data.symbol.Symbol` class stores all information needed to uniquely identify an asset.
- can be used as dict key. 2 symbol objects should be equal when the reference the same asset on the same marked


### Financial Data

- Stored as `pandas.DataFrame` with index `datetime` of type `datetime.datetime`

#### Equities

- columns contain `high`, `open`, `low`, `close` and `volumen`
- might contain additional columns

#### Options

- columns are `puts` and `calls`
- in each column there is a dict with timedelta as keys
- dict entries are dicts themselves mapping from strike price to option price

