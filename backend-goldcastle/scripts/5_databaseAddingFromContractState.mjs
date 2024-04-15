import { groupOfAddress, NodeProvider, web3, subContractId, addressFromContractId, binToHex, contractIdFromAddress, hexToString, stringToHex, encodeByteVec, toApiByteVec, encodeU256, hexToBinUnsafe, encodeHexSignature } from '@alephium/web3'
import pkg from 'pg';
const { Pool } = pkg;
import axios from 'axios';

const pool = new Pool({
  user: 'esse',
  host: 'postgres',
  database: 'goldcastle',
  password: '96509035',
  port: 5432,
});

      ///////                                                         /////////
///////        ALTER SEQUENCE main_nft_index_sequence RESTART WITH 0;        /////////
      ///////                                                         /////////


      async function addToDatabase(result, indexNumber, nftcontractid) {
        const client = await pool.connect();
        try {
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
                        lovercount = $14,
                        anathemacooldown = $15
                    WHERE nftindex = $12
                    AND nftcontractid = $13;  -- Add this condition for nftcontractid
                `;
                const values = [owner, vote, voteTime, wartarget, warstarted, potentialMarriage, marriageTime, feudalLord, feudalTime, anathema, anathemaDeclaredCount, indexNumber, nftcontractid, lovercount, anathemacooldown];
    
                await client.query(query, values);
                console.log(`Values added to the database for index ${indexNumber}`);
            }
        } catch (error) {
            console.error('Error adding to database:', error.message);
        } finally {
            client.release();
        }
    }
    
    //const nodeProvider = new NodeProvider('http://localhost:22973');
    web3.setCurrentNodeProvider("https://lb.notrustverify.ch/");
    const nodeProvider = web3.getCurrentNodeProvider()

    const parentContractId = '68858bfeec8b260a98cef84852cb102eee8f123008edcfbf503a603f63f86000';
    
    (async () => {
        for (let indexNumber = 0; indexNumber <= 562; indexNumber++) {
            try {
                const trypath = encodeU256(indexNumber);
                const group = 0;
                const nftcontractid = subContractId(parentContractId, trypath, group);
    
                const addressToQuery = addressFromContractId(nftcontractid);
    
                const result = await nodeProvider.contracts.getContractsAddressState(addressToQuery, {
                    group: groupOfAddress(addressToQuery),
                });
                console.log(result)
                // Log the immFields
                console.log(`Index ${indexNumber} mutFields:`);
                result.mutFields.forEach((field, index) => {
                    console.log(`mutFields${index + 1} = ${field.value}`);
                });
                await addToDatabase(result, indexNumber, nftcontractid);
                console.log(`Index ${indexNumber} has been processed.`);
                
            } catch (error) {
                console.error(`Error fetching data for index ${indexNumber}:`, error.message);
            }
            await new Promise(resolve => setTimeout(resolve, 3000));
        }
        pool.end();
    })();
