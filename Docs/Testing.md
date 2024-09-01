## Tests to be performed

The tests determined appropriate for the project as of yet can be divided into 2 categories
1. ***Functionality Tests***
2. ***Validatin state machine is still followed***
2. ***Backwards Tests***

### Functionality Tests

1. Driver tests
2. Each function performs as intended
3. Error states are triggered appropriately

### Validation of state machine

Develop a set of ATPs which make sure that the workflow is followed

### Backwards Tests

1. ICD tests to ensure that new meesages developed still run with older versions
2. UI Tests to ensure that older versions of UI still interact with back end
3. Driver tests to ensure new device drivers still interact with older back end

***Note: It is important to define the product lifecycle as at some point after a multiple iterations the software is bound to run out of sync and making it backwards compatible might end up costing more***

## Tests Performed when

Other than basic tests the developer needs to perform when developing their feature the tests defined above need to be incorporated into the V and V cycle

The functionality tests need to be performed during verification phase. And the Validation and Backwards tests need to be performed during the validation phase