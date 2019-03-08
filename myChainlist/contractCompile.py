from web3 import Web3
from solcx import compile_source,compile_files,install_solc 

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545")) # Connecting to the provider Ganache Network

w3.isConnected() # Verify web3 connection

contractSource = '''
pragma solidity ^0.5.5;

contract ChainList {
  // state variables
    address seller;
    string name;
    string description;
    uint256 price;

  // events
    event LogSellArticle(
    address indexed _seller,
    string _name,
    uint256 _price
    );

  // sell an article
    function sellArticle(string memory _name, string memory _description, uint256 _price) public {
        seller = msg.sender;
        name = _name;
        description = _description;
        price = _price;

        emit LogSellArticle(seller, name, price);
    }

  // get an article
    function getArticle() public view returns (
        address _seller,
        string memory _name,
        string memory _description,
        uint256 _price
  ) {
        return(seller, name, description, price);
    }
}
'''

contract_source = compile_files(['ChainList.sol'])
contract=contract_source.pop("ChainList.sol:ChainList")
def deploy_contract(contract_interface):
    # Instantiate and deploy contract
    contract = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']
    )
    # Get transaction hash from deployed contract
    tx_hash = contract.transact(
        transaction={'from': w3.eth.accounts[1]}
    )
    # Get tx receipt to get contract address
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    return tx_receipt['contractAddress']

deploy_contract(contract)
#print(contract_source)
#contract_interface = contract_source['<stdin>:ChainList']


#ChainList = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin']) # Instantiate & Deploy ChainList Contract 