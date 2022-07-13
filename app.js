//importe as bibliotecas de classe
const { sportApi } = require('radar-sport-api');
//contrua as classes
const betfair = new sportApi('betfair', { getCommonContents: false });
const bet365 = new sportApi('bet365', { getCommonContents: false });

betfair.getInfo(
    'Europe:Berlin',
    'stats_season_meta',
    764415
).then((data) => { console.log(data) })
