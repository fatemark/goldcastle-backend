import pkg from 'pg';
const { Pool } = pkg;
import axios from 'axios';
import { groupOfAddress, NodeProvider, web3, subContractId, addressFromContractId, binToHex, contractIdFromAddress, hexToString, stringToHex, encodeByteVec, toApiByteVec, encodeU256, hexToBinUnsafe, encodeHexSignature } from '@alephium/web3';

const pool = new Pool({
    user: 'esse',
    host: 'postgres',
    database: 'goldcastle',
    password: '96509035',
    port: 5432,
});

//const nodeProvider = new NodeProvider('http://localhost:22973');

web3.setCurrentNodeProvider("https://lb.notrustverify.ch/");
const nodeProvider = web3.getCurrentNodeProvider()

const goldtokenid = '0beffdfa642818060ca796ff770bb42d437c93f4f5c381ef89b226ec6ae5f500';
const goldtokenaddress = addressFromContractId(goldtokenid);

(async () => {
    const client = await pool.connect();
    try {


        //////////////////////////////////////////////////////////////////////////////////////////////////////
        const highestNumberQuery = 'SELECT MAX(eventcheckstartnumber) AS max_number FROM goldcastleeventlisteningcheck;';
        const highestNumberResult = await client.query(highestNumberQuery); 
        let highestNumber = highestNumberResult.rows[0].max_number - 1 || 0;  
            ////////////////////////////////////////////////////////////////////////////////////////////////////// set to 0 first time and comment out
            if (highestNumber < 0) {
                highestNumber += 1;
            }
            const step = 5 //give as argument //////////////////////////////////////////////////////////////////////////////////////////////////////

            let startnumber = highestNumber; ////////////////////////////////// 0 first run



            while (step == step) {

            const result = await nodeProvider.events.getEventsContractContractaddress(
                goldtokenaddress, { start: startnumber, limit: step }
            );

            // log result optional
            const expandedresult = JSON.stringify(result, null, 2);
            console.log(expandedresult)
            const events = result.events;

            if (result.events.length == 0) {
                const timenow = parseInt(Date.now() / 1000)
                const saveEndNumberQuery = 'INSERT INTO goldcastleeventlisteningcheck (eventcheckstartnumber, time) VALUES ($1, $2)';
                await client.query(saveEndNumberQuery, [startnumber, timenow]);
                console.log('Inserted new event check numbers successfully');
                return
            }

            for (let event of events) {
                const eventIndex = event.eventIndex;
                const byteVecFields = event.fields.filter(field => field.type === 'ByteVec');
                const U256 = event.fields.filter(field => field.type === 'U256');
                const Address = event.fields.filter(field => field.type === 'Address');
                const txId = event.txId;

                if (eventIndex == 0) {
                    const toaddress = Address[0].value
                    const transferamount = U256[0].value;
                    const jackpotwinnings = U256[1].value;
                    const datetime = Math.floor(Date.now() / 1000)
                    const jackpot = U256[2].value

                    try {
                        // Check if the row with the provided txid already exists
                        const result = await client.query('SELECT COUNT(*) FROM goldwithdraw WHERE txid = $1', [txId]);
                    
                        // If a row with the same txid exists, result.rows[0].count will be greater than 0
                        if (result.rows[0].count > 0) {
                            console.log('Row with the provided txid already exists.');
                            // You can handle the situation where the row already exists, such as logging an error or taking other actions
                        } else {
                            // If the row doesn't exist, insert the new row
                            await client.query('INSERT INTO goldwithdraw (address, wonamount, datetime, txid, jackpot, jackpotwinnings) VALUES ($1, $2, $3, $4, $5, $6)', [
                                toaddress,
                                transferamount,
                                datetime,
                                txId,
                                jackpot,
                                jackpotwinnings
                            ]);
                            console.log('New row inserted successfully.');
                        }
                    } catch (error) {
                        console.error('Error executing SQL query:', error);
                    }
                }


            }

            console.log(result.events.length)
            if (result.events.length == step) {
                startnumber += step
            } else{
                startnumber = startnumber + result.events.length
            try {
                const timenow = parseInt(Date.now() / 1000)
                const saveEndNumberQuery = 'INSERT INTO goldcastleeventlisteningcheck (eventcheckstartnumber, time) VALUES ($1, $2)';
                await client.query(saveEndNumberQuery, [startnumber, timenow]);
                console.log('Inserted new event check numbers successfully');
    
                } catch (error) {
                console.error('Error inserting new event check numbers:', error);
                return
                }
                return;
            }
                
        
        }
                } catch (error) {
                    //console.error('Error executing SQL query:', error.message);
                } finally {
                    client.release();
                    pool.end();
                }
        
            
})();


// event Withdraw(to: Address, transferamount: U256)
// event Won(to: Address, jackpotwinnings: U256)