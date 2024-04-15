import pkg from 'pg';
const { Pool } = pkg;
import {
  groupOfAddress,
  NodeProvider,
  web3,
  subContractId,
  addressFromContractId,
  binToHex,
  contractIdFromAddress,
  hexToString,
  stringToHex,
  encodeByteVec,
  toApiByteVec,
  encodeU256,
  hexToBinUnsafe,
  encodeHexSignature,
} from '@alephium/web3';
import axios from 'axios';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';


const collectionaddress = process.argv[2];

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

web3.setCurrentNodeProvider("https://lb.notrustverify.ch/");
const nodeProvider = web3.getCurrentNodeProvider();

async function querycollection(collectionaddress) {
  try {
    const result = await nodeProvider.contracts.getContractsAddressState(collectionaddress, {
      group: groupOfAddress(collectionaddress),
    });

    if (result.mutFields.length >= 1) {

      let url = ""
      let supply = 0
      let baseuri = ""
      if (collectionaddress == "21ixd5J8qVjcAHkGsSsDTnjcgk85dZLSFvdtiCzYkuqBD") {
        url = hexToString(result.immFields[1].value);
        supply = result.immFields[4].value
        baseuri = hexToString(result.immFields[3].value);

      } else {
      url = hexToString(result.mutFields[1].value);
      supply = result.mutFields[4].value
      baseuri = hexToString(result.mutFields[2].value);
      
    }


      try {
        const response = await axios.get(url);
        const jsonResult = response.data;
        jsonResult.address = collectionaddress;

        const jsonFile = path.join(__dirname, '../jsondata/collections.json');
        let data = { collections: [] };

        try {
          if (fs.existsSync(jsonFile)) {
            const fileContent = fs.readFileSync(jsonFile, 'utf8');
            data = JSON.parse(fileContent);
            if (!data.collections) {
              data.collections = [];
            }
          }
        } catch (error) {
          console.error("Error reading or parsing collections.json:", error);
        }

        jsonResult.supply = supply;
        jsonResult.baseuri = baseuri;

        data.collections.push(jsonResult);
        fs.writeFileSync(jsonFile, JSON.stringify(data, null, 2));

        const collectionName = jsonResult.name;
        process.stdout.write(collectionName);
      } catch (error) {
        console.error("Could not fetch metadata:", error);
      }
    } else {
      console.log("No second immField found.");
    }
  } catch (error) {
    console.error("Error adding collection:", error);
  }
}

querycollection(collectionaddress)