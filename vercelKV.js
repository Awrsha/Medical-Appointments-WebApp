import { kv } from '@vercel/kv';

async function connectToVercelKV() {
  try {
    console.log('Attempting to connect to Vercel KV...');

    if (!process.env.KV_URL || !process.env.KV_REST_API_URL || !process.env.KV_REST_API_TOKEN) {
      throw new Error('Vercel KV environment variables are not set');
    }

    console.log('Environment variables are set correctly');

    await kv.connect();
    console.log('Successfully connected to Vercel KV');

    console.log('Testing connection by setting a value...');
    await kv.set("user_1_session", "session_token_value");
    console.log('Value set successfully');

    console.log('Testing connection by getting the value...');
    const session = await kv.get("user_1_session");
    
    if (session === "session_token_value") {
      console.log('Value retrieved successfully. Connection is fully operational.');
    } else {
      throw new Error('Retrieved value does not match set value');
    }

    return true;
  } catch (error) {
    console.log('Error connecting to Vercel KV:', error.message);
    return false;
  }
}

export { connectToVercelKV };