import { NodeProvider, subContractId, encodeU256, addressFromContractId, web3 } from '@alephium/web3';
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

      /////////                                                         /////////
/////////        ALTER SEQUENCE main_nft_index_sequence RESTART WITH 0;        /////////
      /////////                                                         /////////

      async function addToDatabase(result, nftcontractid, imageurl) {
        const client = await pool.connect();
        try {
          console.log('Adding to database:', result.attributes, 'OldAsiaCollection');
          const nftselfcontractaddress = addressFromContractId(nftcontractid)
          const ageValue = result.attributes.find(attr => attr.trait_type === 'Age')?.value;
          const age = ageValue === '∞' ? 1000000 : (parseInt(ageValue) || null);
          const query = `INSERT INTO nft_goldcastle_asia(nftcontractid, collection, rarity, class, continent, stars, title, domain, subdomain, hp, ap, magic, lives, wisdom, name, age, unique_trait, solo_attack, group_attack, item, allegiance, has_secret, nftselfcontractaddress, nfturi, gender) 
                         VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24, $25)`;
          await client.query(query, [
            nftcontractid,
            'OldAsiaCollection',
            result.attributes.find(attr => attr.trait_type === 'Rarity')?.value || 0,
            result.attributes.find(attr => attr.trait_type === 'Class')?.value || null,
            result.attributes.find(attr => attr.trait_type === 'Continent')?.value || null,
            result.attributes.find(attr => attr.trait_type === 'Stars')?.value || 0,
            result.attributes.find(attr => attr.trait_type === 'Title')?.value || null,
            result.attributes.find(attr => attr.trait_type === 'Domain')?.value || null,
            result.attributes.find(attr => attr.trait_type === 'Subdomain')?.value || null,
            result.attributes.find(attr => attr.trait_type === 'HP')?.value || 0,
            result.attributes.find(attr => attr.trait_type === 'AP')?.value || 0,
            result.attributes.find(attr => attr.trait_type === 'Magic')?.value || 0,
            result.attributes.find(attr => attr.trait_type === 'Lives')?.value || 0,
            result.attributes.find(attr => attr.trait_type === 'Wisdom')?.value || 0,
            result.attributes.find(attr => attr.trait_type === 'Name')?.value || null,
            age,
            result.attributes.find(attr => attr.trait_type === 'Unique trait')?.value || null,
            result.attributes.find(attr => attr.trait_type === 'Solo attack')?.value || null,
            result.attributes.find(attr => attr.trait_type === 'Group attack')?.value || null,
            result.attributes.find(attr => attr.trait_type === 'Item')?.value || null,
            result.attributes.find(attr => attr.trait_type === 'Allegiance')?.value || null,
            result.attributes.find(attr => attr.trait_type === 'Has secret?')?.value || null,
            nftselfcontractaddress,
            imageurl,
            result.attributes.find(attr => attr.trait_type === 'Gender')?.value || null,

          ]);
          
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
          const url = `https://arweave.net/dbdvbcYroy6tjCodD4f4HHgPXmYJGLQdPqPHKNto3v0/${indexNumber}`;
          const imageurl = `https://arweave.net/sm60z3ecwHoErDNEYGXYarM6FZdMbsOvsJkcbU4tnQI/${indexNumber}`
          try {
            const trypath = encodeU256(indexNumber);
            const group = 0;
            const nftcontractid = subContractId(parentContractId, trypath, group);
            const response = await axios.get(url);
            const result = response.data;
            await addToDatabase(result, nftcontractid, imageurl);
            console.log(`Index ${indexNumber} added to the database`);
          } catch (error) {
            console.error(`Error fetching data for index ${indexNumber}:`, error.message);
          }
        }
        
        pool.end();
      })();