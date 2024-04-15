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

web3.setCurrentNodeProvider("https://wallet.mainnet.alephium.org")
const nodeProvider = web3.getCurrentNodeProvider()


//const nodeProvider = new NodeProvider('http://localhost:22973');

const collectionid = '68858bfeec8b260a98cef84852cb102eee8f123008edcfbf503a603f63f86000';
const collectionaddress = addressFromContractId(collectionid);
const collectionname = 'OldAsiaCollection';

(async () => {
    const client = await pool.connect();
    try {

        //////////////////////////////////////////////////////////////////////////////////////////////////////
        const highestNumberQuery = 'SELECT MAX(eventcheckstartnumber) AS max_number FROM minteventlisteningcheck;';
        const highestNumberResult = await client.query(highestNumberQuery); 
        let highestNumber = highestNumberResult.rows[0].max_number - 1 || 0;  

        if (highestNumber < 0) {
            highestNumber += 1;
        }

            const step = 5 

            let startnumber =  highestNumber; 


            while (step == step) {

            const result = await nodeProvider.events.getEventsContractContractaddress(
                collectionaddress, { start: startnumber, limit: step }
            );

            const expandedresult = JSON.stringify(result, null, 2);
            console.log(expandedresult)

            const events = result.events;

            if (result.events.length == 0) {
                const timenow = parseInt(Date.now() / 1000)
                const saveEndNumberQuery = 'INSERT INTO minteventlisteningcheck (eventcheckstartnumber, time) VALUES ($1, $2)';
                await client.query(saveEndNumberQuery, [startnumber, timenow]);
                console.log('Inserted new event check numbers successfully');
                return
            }

            for (let event of events) {
                const eventIndex = event.eventIndex;
                const byteVecFields = event.fields.filter(field => field.type === 'ByteVec');
                const U256 = event.fields.filter(field => field.type === 'U256');
                const Address = event.fields.filter(field => field.type === 'Address');


                if (eventIndex == 0) {

                    const index = U256[0].value;
                    try {
                        await checkContractStateminting(index)
                        console.log(index, startnumber)
                    } catch (error) {
                        console.log('failed to register marriage')
                        return
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
                const saveEndNumberQuery = 'INSERT INTO minteventlisteningcheck (eventcheckstartnumber, time) VALUES ($1, $2)';
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






        async function checkContractStateminting(indexNumber) {
            const client = await pool.connect();

                const url = `https://arweave.net/pAk8Q0NzfBjxoVvE8lQ2RLHbiZUejbRxLSmGa_5v7bQ/${indexNumber}`;
                const imageurl = `https://arweave.net/itP9bEXDGf5214kp4_nNCw9oaEe9bJcy9pVAo7dzR9s/resized/${indexNumber}`

                try {
                  const trypath = encodeU256(indexNumber);
                  const group = 0;
                  const nftcontractid = subContractId(collectionid, trypath, group);
                    console.log('nftcontractid now:', nftcontractid)
                    await checkContractState(addressFromContractId(nftcontractid))

                    } catch (error) {
                        console.log('Failed to add metadata')
                    }
                    
                    finally {
                    client.release();
                    }
                }


                async function checkContractState(address) {
                    const client = await pool.connect();
                    try {
                
                
                        const result = await nodeProvider.contracts.getContractsAddressState(address, {
                            group: groupOfAddress(address),
                        });
                        console.log(result)
                        if (result) {
                            const owner = result.mutFields[0].value;
                            const vote = parseInt(result.mutFields[1].value);
                            const voteTime = parseInt(result.mutFields[2].value);
                            const wartarget = result.mutFields[3].value;
                            const warstarted = parseInt(result.mutFields[4].value);
                            const potentialMarriage = result.mutFields[5].value;
                            const marriageTime = result.mutFields[6].value;
                            const feudalLord = result.mutFields[7].value;
                            const feudalTime = parseInt(result.mutFields[8].value);
                            const anathema = result.mutFields[9].value;
                            const anathemaDeclaredCount = parseInt(result.mutFields[10].value);
                            const lovercount = parseInt(result.mutFields[11].value) || 0;
                            const anathemacooldown = parseInt(result.mutFields[12].value) || 0;
                            const query = `
                                UPDATE nft_goldcastle_asia
                                SET 
                                    owner = $1,
                                    vote = $2,
                                    voteTime = $3,
                                    wartarget = $4,
                                    warstarted = $5,
                                    potentialMarriage = $6,
                                    marriageTime = $7,
                                    feudalLord = $8,
                                    feudalTime = $9,
                                    anathema = $10,
                                    anathemaDeclaredCount = $11,
                                    lovercount = $13,
                                    anathemacooldown = $14
                                WHERE nftselfcontractaddress = $12;  -- Add this condition for nftcontractid
                            `;
                            const values = [owner, vote, voteTime, wartarget, warstarted, potentialMarriage, marriageTime, feudalLord, feudalTime, anathema, anathemaDeclaredCount, address, lovercount, anathemacooldown];
                
                            await client.query(query, values);
                            console.log(`Checked contract state for ${address}`);
                        }
                    } catch (error) {
                        console.error('Error checking contract state:', error.message);
                        return
                    } finally {
                        client.release();
                    }
                }