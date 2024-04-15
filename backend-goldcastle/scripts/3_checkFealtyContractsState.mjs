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


async function checkContractState(address) {
    const client = await pool.connect();
    try {


        const result = await nodeProvider.contracts.getContractsAddressState(address, {
            group: groupOfAddress(address),
        });

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


async function addAnathemaContract(declarerLordAddress, scroundrelAddress, bribe, reason) {
    const client = await pool.connect();
    try {
        const declarerAddress = declarerLordAddress;

        const timedeclared = Date.now()

        const nftcontractid = binToHex(contractIdFromAddress(scroundrelAddress))

        const checkQuery = 'SELECT * FROM anathemacontracts WHERE scroundreladdress = $1 AND hasrunout is NULL';
        const checkResult = await client.query(checkQuery, [scroundrelAddress]);

        // If a row with the same contractAddress exists, delete it
        if (checkResult.rows.length > 0) {
            const deleteQuery = 'DELETE FROM anathemacontracts WHERE scroundreladdress = $1 AND hasrunout is NULL';
            await client.query(deleteQuery, [scroundrelAddress]);
            console.log(`Deleted existing row anathema contract for ${scroundrelAddress}`);
        }

        const declarerquery = 'SELECT name, allegiance, collection, nftindex, members, votingpower, maxpowerpotential, maxdefensivepower, wartargetname, rarity FROM nft_goldcastle_asia WHERE nftselfcontractaddress = $1';
        const declarerqueryresult = await client.query(declarerquery, [declarerAddress]);
        const declarerData = declarerqueryresult.rows[0];
        const { name: declarername, allegiance: declarerallegiance, collection: declarercollection, nftindex: declarernftindex, members: declarermembers, votingpower: declarervotingpower, maxpowerpotential: declarermaxpowerpotential, maxdefensivepower: declarermaxdefensivepower, wartargetname: declarerwartargetname, rarity: declarerrarity } = declarerData;
                

        const nftQuery = 'SELECT nftindex, collection, rarity, name, allegiance, maxpowerpotential, maxdefensivepower, votingpower, overlord, potentialmarriage, unique_trait, members, wartargetname, wife, gender FROM nft_goldcastle_asia WHERE nftcontractid = $1';
        const nftResult = await client.query(nftQuery, [nftcontractid]);
        
        if (nftResult.rows.length === 1) {
            const nftData = nftResult.rows[0];
            const { nftindex, collection, rarity, name, allegiance, maxpowerpotential, maxdefensivepower, votingpower, overlord, potentialmarriage, unique_trait, members, wartargetname, wife, gender } = nftData;
        
            const finalQuery = 'SELECT name, allegiance, collection, nftindex, members, votingpower, maxpowerpotential, maxdefensivepower, wartargetname, rarity FROM nft_goldcastle_asia WHERE nftselfcontractaddress = $1';
            const finalResult = await client.query(finalQuery, [overlord]);
        
            if (finalResult.rows.length > 0) {
                const finalResultData = finalResult.rows[0];
                const { name: overlordname, allegiance: overlordallegiance, collection: overlordcollection, nftindex: overlordnftindex, members: overlordmembers, votingpower: overlordvotingpower, maxpowerpotential: overlordmaxpowerpotential, maxdefensivepower: overlordmaxdefensivepower, wartargetname: overlordwartargetname, rarity: overlordrarity } = finalResultData;
                            
                const query = 'INSERT INTO anathemacontracts (bribe, timedeclared, scroundreladdress, reason, nftindex, collection, rarity, name, allegiance, maxpowerpotential, maxdefensivepower, votingpower, overlord, wife, overlordname, overlordallegiance, overlordcollection, overlordnftindex, unique_trait, members, overlordmembers, overlordvotingpower, overlordmaxpowerpotential, overlordmaxdefensivepower, wartargetname, overlordwartargetname, overlordrarity, gender, declareraddress, declarername, declarerrarity, declarerallegiance, declarercollection, declarernftindex, declarermembers, declarervotingpower, declarermaxpowerpotential, declarermaxdefensivepower, declarerwartargetname) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, $29, $30, $31, $32, $33, $34, $35, $36, $37, $38, $39)';
                await client.query(query, [bribe, timedeclared, scroundrelAddress, reason, nftindex, collection, rarity, name, allegiance, maxpowerpotential, maxdefensivepower, votingpower, overlord, wife, overlordname, overlordallegiance, overlordcollection, overlordnftindex, unique_trait, members, overlordmembers, overlordvotingpower, overlordmaxpowerpotential, overlordmaxdefensivepower, wartargetname, overlordwartargetname, overlordrarity, gender, declarerAddress, declarername, declarerrarity, declarerallegiance, declarercollection, declarernftindex, declarermembers, declarervotingpower, declarermaxdefensivepower, declarermaxpowerpotential, declarerwartargetname]);
            
                const query2 = 'UPDATE nft_goldcastle_asia SET anathemareason = $1, anathematime = $2, anathemadeclarername = $3, anathemabribe = $4, anathemadeclarerrarity = $5, anathemadeclarer = $6 WHERE nftselfcontractaddress = $7';
                await client.query(query2, [reason, timedeclared, declarername, bribe, declarerrarity, declarerAddress, scroundrelAddress]);
                                
            } else {
                console.log('Error: No matching record found in nft_goldcastle_asia table for the overlord.');
            }
        } else {
            console.log('Error: No matching record found in nft_goldcastle_asia table.');
        }
    } catch (error) {
        console.error('Error adding to database:', error.message);
    } finally {
        client.release();
    }
}




async function addFealtyContractToDatabase(bribe, time, lordAddress, minimumClass, lordSubjectIndex, campaign, subjecttarget) {
    const client = await pool.connect();
    try {


        const lordindex = lordSubjectIndex
        const lordaddress = lordAddress

        const checkQuery = 'SELECT * FROM fealtycontracts  WHERE lordsubjectindex = $1 AND lordaddress = $2 AND hasbeenaccepted is NULL';
        const checkResult = await client.query(checkQuery, [lordindex, lordaddress]);

        if (checkResult.rows.length > 0) {
            const deleteQuery = 'DELETE FROM fealtycontracts WHERE lordsubjectindex = $1 AND lordaddress = $2 AND hasbeenaccepted is NULL';
            await client.query(deleteQuery, [lordindex, lordaddress]);
            console.log(`Deleted existing row with contract address ${lordaddress}`);
        }

        const subjectnamequery = 'SELECT name FROM nft_goldcastle_asia WHERE nftselfcontractaddress = $1';
        const subjectnamequeryresult = await client.query(subjectnamequery, [subjecttarget]);
        
        // Extract the 'name' value from the first row of the query result
        const subjectname = subjectnamequeryresult.rows[0].name;
        
        const nftcontractid = binToHex(contractIdFromAddress(lordaddress))

        const nftQuery = 'SELECT nftindex, collection, rarity, name, allegiance, maxpowerpotential, maxdefensivepower, votingpower, overlord, potentialmarriage, unique_trait, members, wartargetname, wife, gender, item, magic, group_attack, solo_attack, class, nfturi FROM nft_goldcastle_asia WHERE nftcontractid = $1';
        const nftResult = await client.query(nftQuery, [nftcontractid]);

        
        if (nftResult.rows.length === 1) {
            const nftData = nftResult.rows[0];
            const { nftindex, collection, rarity, name, allegiance, maxpowerpotential, maxdefensivepower, votingpower, overlord, potentialmarriage, unique_trait, members, wartargetname, wife, gender, item, magic, group_attack, solo_attack, class: classtype, nfturi } = nftData;
            const finalQuery = 'SELECT name, allegiance, collection, nftindex, members, votingpower, maxpowerpotential, maxdefensivepower, wartargetname, rarity, nfturi FROM nft_goldcastle_asia WHERE nftselfcontractaddress = $1';
            const finalResult = await client.query(finalQuery, [overlord]);
        
            if (finalResult.rows.length > 0) {
                const finalResultData = finalResult.rows[0];
                const { name: overlordname, allegiance: overlordallegiance, collection: overlordcollection, nftindex: overlordnftindex, members: overlordmembers, votingpower: overlordvotingpower, maxpowerpotential: overlordmaxpowerpotential, maxdefensivepower: overlordmaxdefensivepower, wartargetname: overlordwartargetname, rarity: overlordrarity, nfturi: overlordnfturi } = finalResultData;

                const query = 'INSERT INTO fealtycontracts (bribe, time, minimumnftclass, lordsubjectindex, lordaddress, campaign, nftindex, collection, rarity, name, allegiance, maxpowerpotential, maxdefensivepower, votingpower, overlord, wife, overlordname, overlordallegiance, overlordcollection, overlordnftindex, unique_trait, members, overlordmembers, overlordvotingpower, overlordmaxpowerpotential, overlordmaxdefensivepower, wartargetname, overlordwartargetname, overlordrarity, gender, subjectname, subjectaddress, item, magic, group_attack, solo_attack, class, nfturi, overlordnfturi) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, $29, $30, $31, $32, $33, $34, $35, $36, $37, $38, $39)';
                await client.query(query, [bribe, time, minimumClass, lordindex, lordaddress, campaign, nftindex, collection, rarity, name, allegiance, maxpowerpotential, maxdefensivepower, votingpower, overlord, wife, overlordname, overlordallegiance, overlordcollection, overlordnftindex, unique_trait, members, overlordmembers, overlordvotingpower, overlordmaxpowerpotential, overlordmaxdefensivepower, wartargetname, overlordwartargetname, overlordrarity, gender, subjectname, subjecttarget, item, magic, group_attack, solo_attack, classtype, nfturi, overlordnfturi ]);
            } else {
                console.log('Error: No matching record found in nft_goldcastle_asia table for the overlord.');
                return
            }
        } else {
            console.log('Error: No matching record found in nft_goldcastle_asia table.');
            return
        }

    } catch (error) {
        console.error('Error adding to database:', error.message);
        return
    } finally {
        client.release();
    }
}

async function registerNewMarriage(proposer, proposee) {
    const client = await pool.connect();

    try {
        // Update proposer's row
        const timenow = Date.now()
        const query1 = `
            UPDATE nft_goldcastle_asia
            SET potentialmarriage = $1, ismarried = true, lovercount = lovercount + 1, marriagetime = $3
            WHERE nftselfcontractaddress = $2
        `;
        await client.query(query1, [proposer, proposee, timenow]);

        // Update proposee's row
        const query2 = `
            UPDATE nft_goldcastle_asia
            SET potentialmarriage = $1, ismarried = true, lovercount = lovercount + 1, marriagetime = $3
            WHERE nftselfcontractaddress = $2
        `;
        await client.query(query2, [proposee, proposer, timenow]);

        console.log('Registered new marriage for ', proposer , 'and ', proposee);
    } catch (error) {
        console.log('Failed to register new marriage for ', proposer , 'and ', proposee);
        return
    }
    client.release();
}


async function addNewMarriageContract(proposer, proposee, dowry, time, loveletter, maxlovercount) {
    const client = await pool.connect();
    try {
        if (proposer, proposee, dowry, time, loveletter, maxlovercount) {

            // Extract values from immFields

            const proposerid = contractIdFromAddress(proposer)
            const contractAddress = subContractId(fealtyid, proposerid, 0)
            const lordaddress = proposer;

            const proposeeQuery = 'SELECT name FROM nft_goldcastle_asia WHERE nftselfcontractaddress = $1';
            const proposeeResult = await client.query(proposeeQuery, [proposee]);
            const proposeedata = proposeeResult.rows[0];
            const { name: proposeename } = proposeedata;

            // Check if a row with the same contractAddress already exists
            const checkQuery = 'SELECT * FROM marriagecontracts WHERE contractaddress = $1';
            const checkResult = await client.query(checkQuery, [contractAddress]);


            if (checkResult.rows.length > 0) {
                const deleteQuery = 'DELETE FROM marriagecontracts WHERE contractaddress = $1 AND hasbeenaccepted is NULL';
                await client.query(deleteQuery, [contractAddress]);
                console.log(`Deleted existing row with contract address ${contractAddress}`);
            }


            const nftcontractid = binToHex(proposerid)

            const nftQuery = 'SELECT nfturi, nftindex, collection, rarity, name, allegiance, maxpowerpotential, maxdefensivepower, votingpower, overlord, potentialmarriage, unique_trait, magic, gender, members FROM nft_goldcastle_asia WHERE nftcontractid = $1';
            const nftResult = await client.query(nftQuery, [nftcontractid]);
            

            if (nftResult.rows.length === 1) {
                const nftData = nftResult.rows[0];
                const { nfturi, nftindex, collection, rarity, name, allegiance, maxpowerpotential, maxdefensivepower, votingpower, overlord, potentialmarriage, unique_trait, magic, gender, members } = nftData;
            
                const finalQuery = 'SELECT name, allegiance, collection, nftindex, members, votingpower, maxpowerpotential, maxdefensivepower, wartargetname, rarity, nfturi FROM nft_goldcastle_asia WHERE nftselfcontractaddress = $1';
                const finalResult = await client.query(finalQuery, [overlord]);


                if (finalResult.rows.length > 0) {
                    const finalResultData = finalResult.rows[0];
                    const { name: overlordname, allegiance: overlordallegiance, collection: overlordcollection, nftindex: overlordnftindex, members: overlordmembers, votingpower: overlordvotingpower, maxpowerpotential: overlordmaxpowerpotential, maxdefensivepower: overlordmaxdefensivepower, wartargetname: overlordwartargetname, rarity: overlordrarity, nfturi: overlordnfturi } = finalResultData;

                    const offercreatetime = Date.now()
                    const query = 'INSERT INTO marriagecontracts (nfturi, contractaddress, dowry, time, proposeraddress, loveletter, nftindex, collection, rarity, name, allegiance, maxpowerpotential, maxdefensivepower, votingpower, overlord, overlordname, overlordallegiance, overlordcollection, overlordnftindex, unique_trait, magic, proposergender, proposee, members, overlordmembers, overlordvotingpower, overlordmaxpowerpotential, overlordmaxdefensivepower, overlordwartargetname, overlordrarity, proposeename, offercreatetime, maxlovercount, overlordnfturi) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, $29, $30, $31, $32, $33, $34)';
                    await client.query(query, [nfturi, contractAddress, dowry, time, lordaddress, loveletter, nftindex, collection, rarity, name, allegiance, maxpowerpotential, maxdefensivepower, votingpower, overlord, overlordname, overlordallegiance, overlordcollection, overlordnftindex, unique_trait, magic, gender, proposee, members, overlordmembers, overlordvotingpower, overlordmaxpowerpotential, overlordmaxdefensivepower, overlordwartargetname, overlordrarity, proposeename, offercreatetime, maxlovercount, overlordnfturi]);
                    console.log('Registered new marriage contract')
                } else {
                    console.log('Error in add marriagecontract: No matching record found in nft_goldcastle_asia table for the overlord.');
                    return
                }
            } else {
                console.log('Error in add marriagecontract: No matching record found in nft_goldcastle_asia table.');
                return
            }
    }
    } catch (error) {
        console.error('Error in add marriagecontract: adding to register marriage contract:', error.message);
        return
    } finally {
        client.release();
    }
}

//const nodeProvider = new NodeProvider('http://localhost:22973');


web3.setCurrentNodeProvider("https://lb.notrustverify.ch/");
const nodeProvider = web3.getCurrentNodeProvider()


const fealtyid = '8805ae3a93cc73766aa8bbf1deb83814798924acb23be5e1e328dd904d247f00';
const fealtyaddress = addressFromContractId(fealtyid);

(async () => {
    const client = await pool.connect();
    try {


        //////////////////////////////////////////////////////////////////////////////////////////////////////
        const highestNumberQuery = 'SELECT MAX(eventcheckstartnumber) AS max_number FROM eventlisteningcheck;';
        const highestNumberResult = await client.query(highestNumberQuery); 
        let highestNumber = highestNumberResult.rows[0].max_number - 1 || 0;  
            ////////////////////////////////////////////////////////////////////////////////////////////////////// set to 0 first time and comment out
            if (highestNumber < 0) {
                highestNumber += 1;
            }
            
        const step = 5; //give as argument //////////////////////////////////////////////////////////////////////////////////////////////////////


            let startnumber = 0 //  highestNumber; //////////////////////////////////  0 first run



            while (step == step) {

            const result = await nodeProvider.events.getEventsContractContractaddress(
                fealtyaddress, { start: startnumber, limit: step }
            );
            
            console.log(startnumber)

            const expandedresult = JSON.stringify(result, null, 2);
            // console.log(expandedresult);
            
            const events = result.events;


            if (result.events.length == 0) {
                const timenow = parseInt(Date.now() / 1000)
                const saveEndNumberQuery = 'INSERT INTO eventlisteningcheck (eventcheckstartnumber, time) VALUES ($1, $2)';
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

                    const proposer = Address[0].value;
                    const proposee = Address[1].value;

                    try {
                        await registerNewMarriage(proposer, proposee)

                    } catch (error) {
                        console.log('failed to register marriage')
                        return
                    }

                }

                else if (eventIndex == 1) {

                    const proposer = Address[0].value;
                    const proposee = Address[1].value;
                    const dowry = U256[0].value;
                    const time = U256[1].value;
                    const loveletter = byteVecFields[0].value;
                    const maxlovercount = U256[2].value;

                    try {
                        await addNewMarriageContract(proposer, proposee, dowry, time, loveletter, maxlovercount)
                        } catch (error) {
                            console.log('failed to register marriage contract')
                            return
                        }

                }

                else if (eventIndex == 2) {

                    const proposer = Address[0].value;
                    const proposee = Address[1].value;

                    try {
                        await registerNewMarriage(proposer, proposee)

                        const query = `
                        UPDATE marriagecontracts
                        SET hasbeenaccepted = true
                        WHERE proposeraddress = $1
                        `;
                        await client.query(query, [proposer]);

                        console.log('Registered marriage with paid dowry')

                    } catch (error) {
                        console.log('failed to register marriage')
                        return
                    }


                }


                else if (eventIndex == 3) {

                    const proposer = Address[0].value;
                    try {
                        const query = `
                        UPDATE marriagecontracts
                        SET hasbeenaccepted = false
                        WHERE proposeraddress = $1 AND hasbeenaccepted IS NULL
                        `;
                        await client.query(query, [proposer]);

                        console.log('Marriage offer rescinded')

                    } catch (error) {
                        console.log('failed to rescind marriage')
                        return
                    }
                }



                else if (eventIndex == 4) {

                    const wifeHusband = Address[0].value;
                    const claimant = Address[1].value;

                    try {
                        const query = `
                        UPDATE nft_goldcastle_asia
                        SET potentialmarriage = $1, ismarried = false
                        WHERE nftselfcontractaddress = $2
                    `;
                    await client.query(query, [wifeHusband, wifeHusband]);

                        const query2 = `
                        UPDATE nft_goldcastle_asia
                        SET potentialmarriage = $1, ismarried = false
                        WHERE nftselfcontractaddress = $2
                    `;
                    await client.query(query2, [claimant, claimant]);

                        console.log('Divorce registered')

                    } catch (error) {
                        console.log('failed to register divorce')
                        return
                    }

                }


                else if (eventIndex == 5) {
                    //become lover
                }

                else if (eventIndex == 6) {

                    const bribe = U256[0].value;
                    const time = U256[1].value;
                    const lordAddress = Address[0].value;
                    const minimumClass = U256[2].value;
                    const lordSubjectIndex = U256[3].value;
                    const campaign = byteVecFields[0].value;
                    const subjecttarget = Address[1].value;
                    //console.log('trying')
                    try {
                         await addFealtyContractToDatabase(bribe, time, lordAddress, minimumClass, lordSubjectIndex, campaign, subjecttarget)
                } catch (error) {
                    console.log('failed to register new fealty for gold contract offer')
                    return
                }
                }

                else if (eventIndex == 7) {
                
                    const lordAddress = Address[0].value;
                    const subjectAddress = Address[1].value;
                    const lordSubjectIndex = U256[0].value;
                    console.log(lordAddress, subjectAddress, lordSubjectIndex)
                    try {

                        const query = `
                        UPDATE fealtycontracts
                        SET hasbeenaccepted = true
                        WHERE lordaddress = $1 AND lordsubjectindex = $2
                        `;
                        await client.query(query, [lordAddress, lordSubjectIndex]);

                        await checkContractState(subjectAddress)

                    } catch (error) {
                            console.log('failed to check contract state')
                            return
                        }
                }

                else if (eventIndex == 8) {
                                
                    const subjectAddress = Address[1].value;

                    try {

                        await checkContractState(subjectAddress)

                    } catch (error) {
                            console.log('failed to check contract state for new free fealty swearing')
                            return
                        }
                }



                else if (eventIndex == 9) {

                    const lordAddress = Address[0].value;
                    const lordSubjectIndex = U256[0].value
                    try {
                        const query = `
                        UPDATE fealtycontracts
                        SET hasbeenaccepted = false
                        WHERE lordaddress = $1 AND lordsubjectindex = $2 AND hasbeenaccepted IS NULL
                        `;
                        await client.query(query, [lordAddress, lordSubjectIndex]);

                        console.log('Fealty offer rescinded')

                    } catch (error) {
                        console.log('failed to rescind fealty offer')
                        return
                    }
                }


                else if (eventIndex == 10) {
                    console.log('trying')

                    const declarerLordAddress = Address[0].value;
                    const scroundrelAddress = Address[1].value;
                    const bribe = U256[0].value;
                    const reason = byteVecFields[0].value;

                    try {
                        await addAnathemaContract(declarerLordAddress, scroundrelAddress, bribe, reason)
                        await checkContractState(scroundrelAddress)
                        await checkContractState(declarerLordAddress)
                } catch (error) {
                    console.log('failed to register new Anathema by Higher Lord')
                    return
                }
                }


                else if (eventIndex == 11) {
                    console.log('trying')

                    const declarerLordAddress = Address[0].value;
                    const scroundrelAddress = Address[1].value;
                    const bribe = U256[0].value;
                    const reason = byteVecFields[0].value;

                    try {
                        await addAnathemaContract(declarerLordAddress, scroundrelAddress, bribe, reason)
                        await checkContractState(scroundrelAddress)
                        await checkContractState(declarerLordAddress)
                } catch (error) {
                    console.log('failed to register new Anathema by Lord')
                    return
                }
                }


                else if (eventIndex == 12) {

                    const revokerAddress = Address[0].value;
                    const scroundrelAddress = Address[1].value;

                    try {

                        const declarerquery = 'SELECT declarername FROM anathemacontracts WHERE scroundreladdress = $1 AND (hasrunout IS NULL OR hasrunout = false)';
                        const declarerqueryresult = await client.query(declarerquery, [scroundrelAddress]);
                        const declarerData = declarerqueryresult.rows[0];
                        const { declarername } = declarerData;

                        const query = `
                        UPDATE anathemacontracts
                        SET revokername = $3, revokeraddress = $4, hasrunout = true
                        WHERE scroundreladdress = $1 AND declareraddress = $2
                        `;
                        await client.query(query, [scroundrelAddress, revokerAddress, declarername, revokerAddress]);

                        await checkContractState(scroundrelAddress)
                        await checkContractState(revokerAddress)
                } catch (error) {
                    console.log('failed to register the revocation of Anathema by declarer')
                    return
                }
                }



                else if (eventIndex == 13) {

                    const revokerAddress = Address[0].value;
                    const scroundrelAddress = Address[1].value;

                    try {

                        const declarerquery = 'SELECT declareraddress FROM anathemacontracts WHERE scroundreladdress = $1 AND (hasrunout IS NULL OR hasrunout = false)';
                        const declarerqueryresult = await client.query(declarerquery, [scroundrelAddress]);
                        const declarerData = declarerqueryresult.rows[0];
                        const { declareraddress } = declarerData;
    
                        const revokerquery = 'SELECT name FROM nft_goldcastle_asia WHERE nftselfcontractaddress = $1';
                        const revokerqueryresult = await client.query(revokerquery, [revokerAddress]);
                        const revokerData = revokerqueryresult.rows[0];
                        const { name } = revokerData;

                        const query = `
                        UPDATE anathemacontracts
                        SET revokername = $3, revokeraddress = $4, hasrunout = true
                        WHERE scroundreladdress = $1 AND declareraddress = $2
                        `;
                        await client.query(query, [scroundrelAddress, declareraddress, name, revokerAddress]);

                        await checkContractState(scroundrelAddress)
                        await checkContractState(declareraddress)
                } catch (error) {
                    console.log('failed to register the revocation of Anathema by high lord')
                    return
                }
                }


                else if (eventIndex == 14) {
                    const scroundrelAddress = Address[0].value;
                    const revokerAddress = Address[1].value;

                    try {

                        const declarerquery = 'SELECT declareraddress FROM anathemacontracts WHERE scroundreladdress = $1 AND (hasrunout IS NULL OR hasrunout = false)';
                        const declarerqueryresult = await client.query(declarerquery, [scroundrelAddress]);
                        const declarerData = declarerqueryresult.rows[0];
                        const { declareraddress } = declarerData;

                        const revokerquery = 'SELECT name FROM nft_goldcastle_asia WHERE nftselfcontractaddress = $1';
                        const revokerqueryresult = await client.query(revokerquery, [revokerAddress]);
                        const revokerData = revokerqueryresult.rows[0];
                        const { name } = revokerData;

                        const query = `
                        UPDATE anathemacontracts
                        SET revokername = $3, revokeraddress = $4, hasrunout = true, bribepaid = true
                        WHERE scroundreladdress = $1 AND declareraddress = $2
                        `;
                        await client.query(query, [scroundrelAddress, declareraddress, name, revokerAddress]);

                        await checkContractState(scroundrelAddress)
                        await checkContractState(declareraddress)
                } catch (error) {
                    console.log('failed to register the revocation of Anathema by bribe')
                    return
                }
                }


                else if (eventIndex == 15) {
                    const scroundrelAddress = Address[0].value;

                    try {

                        const declarerquery = 'SELECT declareraddress FROM anathemacontracts WHERE scroundreladdress = $1 AND (hasrunout IS NULL OR hasrunout = false)';
                        const declarerqueryresult = await client.query(declarerquery, [scroundrelAddress]);
                        const declarerData = declarerqueryresult.rows[0];
                        const { declareraddress } = declarerData;
                        const name = 'time';
                        
                        const query = `
                        UPDATE anathemacontracts
                        SET revokername = $3, revokeraddress = $4, hasrunout = true, revokedbytime = true
                        WHERE scroundreladdress = $1 AND declareraddress = $2
                        `;
                        await client.query(query, [scroundrelAddress, declareraddress, name, scroundrelAddress]);

                        await checkContractState(scroundrelAddress)
                        await checkContractState(declareraddress)
                } catch (error) {
                    console.log('failed to register the revocation of Anathema by time')
                    return
                }
                }



                else if (eventIndex == 16) {

                    const declarerAddress = Address[0].value;
                    const targetAddress = Address[1].value;
                    const timedeclared = U256[0].value;

                    try {

                        const warquery = 'SELECT name FROM nft_goldcastle_asia WHERE nftselfcontractaddress = $1';
                        const warqueryresult = await client.query(warquery, [targetAddress]);
                        const warData = warqueryresult.rows[0];
                        const { name } = warData;

                        const query = `
                        UPDATE nft_goldcastle_asia
                        SET warstarted = $1, wartarget = $2, isatwar = true, wartargetname = $3
                        WHERE nftselfcontractaddress = $4
                        `;
                        await client.query(query, [timedeclared, targetAddress, name, declarerAddress]);

                } catch (error) {
                    console.log('failed to register declaration of war')
                    return
                }
                }


                else if (eventIndex == 17) {

                    const voterId = byteVecFields[0].value;
                    const voteInput = U256[0].value;
                    const voteTime = U256[1].value;

                    try {

                        const query = `
                        UPDATE nft_goldcastle_asia
                        SET vote = $1, votetime = $2
                        WHERE nftcontractid = $3
                        `;
                        await client.query(query, [voteInput, voteTime, voterId]);

                        /// start electionchecker
                    
                } catch (error) {
                    console.log('failed to register vote')
                    return
                }
                }



                else if (eventIndex == 18) {

                    const lordAddress = Address[0].value;

                    try {

                        const query = `
                        UPDATE nft_goldcastle_asia
                        SET feudallord = $1, overlord = $2, isoverlord = True
                        WHERE nftselfcontractaddress = $3
                        `;
                        await client.query(query, [lordAddress, lordAddress, lordAddress]);

                        /// start overlordchecker
                    
                } catch (error) {
                    console.log('failed to register new overlord')
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
            const saveEndNumberQuery = 'INSERT INTO eventlisteningcheck (eventcheckstartnumber, time) VALUES ($1, $2)';
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






// events fealty with event (__eventindex__)
// event NewMarriage(proposer: Address, proposee: Address) event 0
// event NewMarriageContractOffer(proposer: Address, proposee: Address, dowry: U256, time: U256, loverletter: ByteVec, maxlovercount: U256) event 1
// event NewMarriageWithDowry(proposer: Address, proposee: Address) event 2
// event RescindMarriage(proposer: Address) event 3
// event Divorce(wifeHusband: Address, claimant: Address) event 4

// event BecomeLover(selfloverAddress: Address, lovertargetAddress: Address) 5 ///add

// event NewFealtyContract(bribe: U256, time: U256, lordAddress: Address, minimumClass: U256, lordSubjectIndex: U256, campaign: ByteVec, subjecttarget: Address) event 6
// event NewSwearForGold(lordAddress: Address, subjectAddress: Address, lordSubjectIndex: U256) event 7
// event NewSwearForFree(lordAddress: Address, subjectAddress: Address, time: U256) 8
// event NewRescindGoldFealtyOffer(lordAddress: Address, lordSubjectIndex: U256) event 9
// event NewDeclareAnathemaByHigherLord(declarerLordAddress: Address, scroundrelAddress: Address, bribe: U256, reason: ByteVec) event 10
// event NewDeclareAnathemaByLord(declarerLordAddress: Address, scroundrelAddress: Address, bribe: U256, reason: ByteVec) event 11
// event NewRevokeAnathemaByDeclarer(revokerAddress: Address, scroundrelAddress: Address) event 12
// event NewRevokeAnathemaByHighLord(revokerAddress: Address, scroundrelAddress: Address) event 13
// event NewRevokeAnathemaByBribe(scroundrelAddress: Address, lordAddress: Address) event 14
// event NewRevokeAnathemaByTime(scroundrelAddress: Address) event 15
// event WarDeclared(declarerAddress: Address, targetAddress: Address, timenow: U256) event 16
// event Voted(voterId: ByteVec, voteInput: U256, voteTime: U256) event 17

// event BecameOverlord(lordAddress: Address) event 18




//// Checking all possible fealty contracts:

// (async () => {
//     const client = await pool.connect();
//     try {


        
//         const res = await client.query('SELECT nftcontractid FROM nft_goldcastle_asia');
//         const rows = res.rows;

//         for (const row of rows) {
//             const nftcontractid = row.nftcontractid;

//             for (let index = 0; index <= 6; index++) {
//                 try {
//                     const lordNftId = hexToBinUnsafe(nftcontractid);
//                     const lordSubjectIndex = encodeU256(index);

//                     const totalLength = lordSubjectIndex.length + lordNftId.length + fealtyforgoldid.length;
//                     const pathof = new Uint8Array(totalLength);
//                     let offset = 0;
//                     pathof.set(lordSubjectIndex, offset);
//                     offset += lordSubjectIndex.length;
//                     pathof.set(lordNftId, offset);
//                     offset += lordNftId.length;
//                     pathof.set(fealtyforgoldid, offset);

//                     const subContractIdTarget = subContractId(fealtyid, pathof, 0);
//                     const subContractAddressTarget = addressFromContractId(subContractIdTarget);

//                     const result = await nodeProvider.contracts.getContractsAddressState(subContractAddressTarget, {
//                         group: groupOfAddress(subContractAddressTarget),
//                     });

//                     await addToDatabase(result, nftcontractid, index, subContractAddressTarget);
//                     console.log(`Processed nftcontractid ${nftcontractid} for index ${index}`);

//                 } catch (error) {
//                     //console.error(`Error fetching data for nftcontractid ${nftcontractid} at index ${index}:`, error.message);
//                 }
//             }
//         }
//     } catch (error) {
//         //console.error('Error executing SQL query:', error.message);
//     } finally {
//         client.release();
//         pool.end();
//     }
// })();