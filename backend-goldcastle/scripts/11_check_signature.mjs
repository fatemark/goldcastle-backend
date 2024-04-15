import { verifySignature, hashMessage, addressFromPublicKey, web3 } from "@alephium/web3";
import pkg from 'pg';
const { Pool } = pkg;
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

web3.setCurrentNodeProvider("https://lb.notrustverify.ch/");
const nodeProvider = web3.getCurrentNodeProvider();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const pool = new Pool({
  user: 'esse',
  host: 'postgres',
  database: 'goldcastle',
  password: '96509035',
  port: 5432,
});

const publicKey = process.argv[2];
const signature = process.argv[3];
const message = process.argv[4];

async function checksignature(publicKey, signature, message) {
  const client = await pool.connect();

  try {
    const hash = hashMessage(message, "blake2b");
    const istrue = verifySignature(hash, publicKey, signature);
    console.log(istrue);


    const address = addressFromPublicKey(publicKey);

    if (istrue) {
      console.log('Signature verified');
      const discordidquery = 'SELECT discordid FROM owners WHERE publickey = $1';
      const result = await client.query(discordidquery, [publicKey]);
      const discordid = result.rows[0].discordid;
      console.log(discordid)
    
      const addQuery = `
        UPDATE nft_goldcastle_asia 
        SET discordid = $1 
        WHERE owner = $2
      `;
      await client.query(addQuery, [discordid, address]);
      console.log('Updated discord ids');
    
        let goldBalance = 0
        try {
        
         web3.setCurrentNodeProvider("https://lb.notrustverify.ch/");;
        const nodeProvider = web3.getCurrentNodeProvider();

        // Make the API call to get the balance
        const balanceResult = await nodeProvider.addresses.getAddressesAddressBalance(address);

        const goldTokenId = '0beffdfa642818060ca796ff770bb42d437c93f4f5c381ef89b226ec6ae5f500';
        const goldBalanceQuery = balanceResult.tokenBalances.find(token => token.id === goldTokenId);
        goldBalance = goldBalanceQuery.amount;
        } catch {
            goldBalance = 0
            console.log("Zero Gold for this pour soul") 
        }

        console.log("Your balance sirr",goldBalance)
        if (goldBalance != null) {
            console.log(`Gold token balance: ${goldBalance}`);
          
            // Check if the owner already exists in the table
            const checkOwnerQuery = "SELECT * FROM goldowners WHERE discordid = $1";
            const result = await client.query(checkOwnerQuery, [discordid]);
          
            if (result.rows.length > 0) {
              // Discord id  exists, update the existing row
              const updateOwnerQuery = "UPDATE goldowners SET goldbalance = $1, owner = $2 WHERE discordid = $3";
              await client.query(updateOwnerQuery, [goldBalance, address, discordid]);
              console.log('Updated gold balance and owner for existing discord id');
            } else {
              // Discord id doesn't exist, insert a new row
              const addOwnerQuery = "INSERT INTO goldowners (owner, goldbalance, discordid) VALUES ($1, $2, $3)";
              await client.query(addOwnerQuery, [address, goldBalance, discordid]);
              console.log('Inserted new owner with gold balance and Discord ID');
            }
          } else {
            console.log('Gold token not found in the balance.');
          }

          try{
            updateBalances(address, discordid)
          } catch {
            console.log("Could not update other balances: ", error)
          }
    }



    const deleteQuery = 'DELETE FROM owners WHERE address = $1';
    await client.query(deleteQuery, [address]);
    console.log(`Deleted row`);

    client.release(); 
  } catch (error) {
    console.log('Could not enter discordid into the database');
    console.error(error); // Log the error for debugging purposes
  }
}

async function checkbalances() {
  const jsonFile = path.join(__dirname, '/discord/jsondata/tokenlist.json');
  let data = { tokens: [] };

  try {
      if (fs.existsSync(jsonFile)) {
          const fileContent = fs.readFileSync(jsonFile, 'utf8');
          data = JSON.parse(fileContent);
      }
  } catch (error) {
      console.error("Error reading or parsing tokenlist.json:", error);
  }

  const tokenamount = data.tokens.length;
  const tokenids = []
  const tokensymbols = []
  const decimals = []

  let n = tokenamount - 1
  while (n >= 0) {

  tokensymbols.push(data.tokens[n].symbol)
  tokenids.push(data.tokens[n].id)
  decimals.push(data.tokens[n].decimals)
  n -= 1
  }

  return [tokensymbols, tokenids, tokenamount, decimals]
}

async function updateBalances(address, discordid) {
  const client = await pool.connect();
  try {
        const [tokensymbols, tokenids, tokenamount, decimals] = await checkbalances();

        console.log(tokensymbols)
        console.log(tokenids)
        console.log(tokenamount)
        console.log(decimals)

          try {
              const balanceResult = await nodeProvider.addresses.getAddressesAddressBalance(address);

              const balanceresults = []
              let n = tokenamount - 1

              while ( n >= 0) {

              const balanceQuery = balanceResult.tokenBalances.find(token => token.id === tokenids[n]);
              let amount = balanceQuery ? balanceQuery.amount : 0;
              
              if (decimals[n] == 0) {
                amount = parseInt(amount)
              } else {
                amount = parseInt( amount / (10 ** decimals[n]))
              }

              await client.query(`UPDATE goldowners SET "${tokensymbols[n]}" = $1 WHERE owner = $2`, [amount, address]);
              n -= 1
              }
              console.log(`Updated TOKEN balances for address ${address} }`);


              const idsWithAmountOne = balanceResult.tokenBalances?.filter(token => token.amount === '1').map(token => token.id);

              const nftlength = idsWithAmountOne.length;
              n = nftlength - 1
              while ( n >= 0) {
                  await client.query(`UPDATE allnfts SET owner = $1, discordid = $2 WHERE nftcontractid = $3`, [address, discordid, idsWithAmountOne[n]]);
                  n -= 1
              }

          } catch (error) {
              console.error("Error fetching balances:", error);
              return 0;
          }

      
  } catch (error) {
      console.error("Error updating balances:", error);
  } finally {
      client.release(); // Release the client back to the pool
  }
}


checksignature(publicKey, signature, message);