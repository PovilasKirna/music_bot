const { Client, Intents, Collection } = require('discord.js');

const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES] });
 
const prefix = '-';
 
const fs = require('fs');


const {
	joinVoiceChannel,
	createAudioPlayer,
	createAudioResource,
	entersState,
	StreamType,
	AudioPlayerStatus,
	VoiceConnectionStatus} = require('@discordjs/voice');

const player = createAudioPlayer();
import { createDiscordJSAdapter } from './adapter';

 
client.commands = new Collection();
 
const commandFiles = fs.readdirSync('./commands/').filter(file => file.endsWith('.js'));
for(const file of commandFiles){
    const command = require(`./commands/${file}`);
 
    client.commands.set(command.name, command);
}
 
 
client.once('ready', () => {
    console.log('Codelyon is online!');
});
 
client.on('message', message =>{
    if(!message.content.startsWith(prefix) || message.author.bot) return;
 
    const args = message.content.slice(prefix.length).split(/ +/);
    const command = args.shift().toLowerCase();
 
    if(command === 'ping'){
        client.commands.get('ping').execute(message, args);
    } else if (command === 'play'){
        client.commands.get('play').execute(message, args, client);
    }
});
 
client.login('ODkxODI1NDEzOTQ3NTM1NDAx.YVD_JA.-R3yOjXLjYaxQagZP0uMH-Ez4tw');