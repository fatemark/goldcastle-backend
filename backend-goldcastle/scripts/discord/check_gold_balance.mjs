import pkg from 'pg';
const { Pool } = pkg;
import { groupOfAddress, NodeProvider, web3, subContractId, addressFromContractId, binToHex, contractIdFromAddress, hexToString, stringToHex, encodeByteVec, toApiByteVec, encodeU256, hexToBinUnsafe, encodeHexSignature } from '@alephium/web3';

const pool = new Pool({
    user: 'esse',
    host: 'postgres',
    database: 'goldcastle',
    password: '96509035',
    port: 5432,
});

const goldTokenId = '0beffdfa642818060ca796ff770bb42d437c93f4f5c381ef89b226ec6ae5f500';

web3.setCurrentNodeProvider("https://lb.notrustverify.ch/");
const nodeProvider = web3.getCurrentNodeProvider();

async function getGoldBalance(address) {
    try {
        const balanceResult = await nodeProvider.addresses.getAddressesAddressBalance(address);
        const goldBalanceQuery = balanceResult.tokenBalances.find(token => token.id === goldTokenId);
        return goldBalanceQuery ? goldBalanceQuery.amount : 0;
    } catch (error) {
        console.error("Error fetching gold balance:", error);
        return 0;
    }
}

async function updateGoldBalances() {
    const client = await pool.connect();
    try {
        // Select all addresses from the goldowners table
        const addressesQuery = await client.query('SELECT owner FROM goldowners');

        // Iterate over each address and update gold balance
        for (const row of addressesQuery.rows) {
            const address = row.owner;
            const goldBalance = await getGoldBalance(address);
            
            // Update gold balance in the goldowners table
            await client.query('UPDATE goldowners SET goldbalance = $1 WHERE owner = $2', [goldBalance, address]);
            console.log(`Updated gold balance for address ${address} to ${goldBalance}`);
        }
    } catch (error) {
        console.error("Error updating gold balances:", error);
    } finally {
        client.release(); // Release the client back to the pool
    }
}

// Call the function to update gold balances
updateGoldBalances();
