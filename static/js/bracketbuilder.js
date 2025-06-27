const styles = {
    game: 'game',
    pendingGame: 'pending',
    completedGame: 'completed',
    divisionMember: 'member',
    selectedGame: 'selected',
    relatedGame: 'related',
};

class Ajax {
    static fetchSites() { return this._rawSites().map(site => new Site(site)); }
    static _rawSites() { return [ 
        {
            id:0, name: "Site 1", number: 1,  
            areas: ['Area1', 'Area2', 'Area3', 'Area4', 'Area5', 'Area6'],
            slots: [ '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM',
                '1:00 PM', '2:00 PM', '3:00 PM' ],
        },
        {
            id: 1, name: "Site 2", number: 2,
            areas: ['Area1', 'Area2'], 
            slots: [ '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', 
                '1:00 PM', '2:00 PM', '3:00 PM' ],
        } ];
    }
    static _rawDivisions() {
        return [ 
            {
                id: null, number: 1, name: "Division 1", bracketType: 0, loserBracket: false, selectedGame: 3,
                games: [
                    {
                        id: null, number: 1, division: 1,
                        teamRed: "Team 1", teamBlue: "Team 2",
                        parents: [], children: [5, 7],
                        pending: false, completed: true, winner: 0,
                        site: 0, area: 0, slot: 0,
                    },

                    { 
                        id: null, number: 2, division: 1,
                        teamRed: "Team 3", teamBlue: "Team 4",
                        parents: [], children: [5, 7],
                        pending: false, completed: false, winner: null, 
                        site: 0, area: 1, slot: 0, 
                    },

                    {
                        id: null, number: 3, division: 1,
                        teamRed: "Team 5", teamBlue: "Team 6", 
                        parents: [], children: [6, 7],
                        pending: true, completed: false, winner: null,
                        site: 0, area: 1, slot: 1, 
                    },

                    {
                        id: null, number: 4, division: 1,
                        teamRed: "Team 7", teamBlue: "Team 8", 
                        parents: [], children: [6, 7],
                        pending: true, completed: false, winner: null, 
                        site: 0, area: 0, slot: 1, 
                    },

                    { 
                        id: null, number: 5, division: 1,
                        teamRed: "Team 1", teamBlue: "Winner Game 2", 
                        parents: [1, 2], children: [7],
                        pending: true, completed: false, winner: null, 
                        site: 0, area: 0, slot: 3, 
                    },
                    {
                        id: null, number: 6, division: 1,
                        teamRed: "Winner Game 3", teamBlue: "Winner Game 4", 
                        parents: [3, 4], children: [7],
                        pending: true, completed: false, winner: null, 
                        site: 0, area: 1, slot: 3,
                    },
                    {
                        id: null, number: 7, division: 1,
                        teamRed: "Winner Game 5", teamBlue: "Winner Game 6", 
                        parents: [1, 2, 3, 4, 5, 6], children: [],
                        pending: true, completed: false, winner: null, 
                        site: 0, area: 1, slot: 5,
                    },
                ],
            }, 
            {
                id: null, number: 2, name: "Division 2", bracketType: 0, loserBracket: false, selectedGame: 1,
                games: [
                    {
                        id: null, number: 1, division: 2,
                        teamRed: "Team 1", teamBlue: "Team 2",
                        parents: [], children: [5, 7],
                        pending: false, completed: true, winner: 0,
                        site: 0, area: 2, slot: 0,
                    },

                    { 
                        id: null, number: 2, division: 2,
                        teamRed: "Team 3", teamBlue: "Team 4",
                        parents: [], children: [5, 7],
                        pending: false, completed: false, winner: null, 
                        site: 0, area: 3, slot: 0, 
                    },

                    {
                        id: null, number: 3, division: 2,
                        teamRed: "Team 5", teamBlue: "Team 6", 
                        parents: [], children: [6, 7],
                        pending: false, completed: false, winner: null,
                        site: 0, area: 4, slot: 0, 
                    },

                    {
                        id: null, number: 4, division: 2,
                        teamRed: "Team 7", teamBlue: "Team 8", 
                        parents: [], children: [6, 7],
                        pending: false, completed: false, winner: null, 
                        site: 0, area: 5, slot: 0, 
                    },

                    { 
                        id: null, number: 5, division: 2,
                        teamRed: "Team 1", teamBlue: "Winner Game 2", 
                        parents: [1, 2], children: [7],
                        pending: true, completed: false, winner: null, 
                        site: 0, area: 0, slot: 2, 
                    },
                    {
                        id: null, number: 6, division: 2,
                        teamRed: "Winner Game 3", teamBlue: "Winner Game 4", 
                        parents: [3, 4], children: [7],
                        pending: true, completed: false, winner: null, 
                        site: 0, area: 1, slot: 2,
                    },
                    {
                        id: null, number: 7, division: 2,
                        teamRed: "Winner Game 5", teamBlue: "Winner Game 6", 
                        parents: [1, 2, 3, 4, 5, 6], children: [],
                        pending: true, completed: false, winner: null, 
                        site: 0, area: 0, slot: 4,
                    },
                ],
            },
            {
                id: null, number: 3, name: "Division 3", bracketType: 3, loserBracket: false, selectedGame: 1,
                games: [
                    { 
                        id: null, number: 1, division: 3,
                        teamRed: "Team 1", teamBlue: "Team 2", 
                        parents: [], children: [3, 4, 5, 6],
                        pending: false, completed: false, winner: null, 
                        site: 0, area: 2, slot: 1, 
                    },
                    { 
                        id: null, number: 2, division: 3,
                        teamRed: "Team 3", teamBlue: "Team 4", 
                        parents: [], children: [3, 4, 5, 6],
                        pending: false, completed: false, winner: null, 
                        site: 0, area: 2, slot: 2, 
                    },
                    { 
                        id: null, number: 3, division: 3,
                        teamRed: "Team 1", teamBlue: "Team 3", 
                        parents: [1, 2], children: [5, 6],
                        pending: false, completed: false, winner: null, 
                        site: null, area: null, slot: null, 
                    },
                    { 
                        id: null, number: 4, division: 3,
                        teamRed: "Team 2", teamBlue: "Team 4", 
                        parents: [1, 2], children: [5, 6],
                        pending: false, completed: false, winner: null, 
                        site: 0, area: 0, slot: 5,
                    },
                    {
                        id: null, number: 5, division: 3,
                        teamRed: "Team 1", teamBlue: "Team 4",
                        parents: [1, 2, 3, 4], children: [],
                        pending: false, completed: false, winner: null,
                        site: 0, area: 0, slot: 7,
                    },
                    {
                        id: null, number: 6, division: 3,
                        teamRed: "Team 2", teamBlue: "Team 3",
                        parents: [1, 2, 3, 4], children: [],
                        pending: false, completed: false, winner: null,
                        site: 0, area: 1, slot: 7,
                    },
                ],
            }
        ];
    }
    static gamesChangeBracketType(divisionId, bracketType) { return [] }
    static fetchDivisions() { return this._rawDivisions().map(division => new Division(division)); }
}

class Site {
    constructor(data) {
        this.id = data.id;
        this.number = data.number;
        this.name = data.name;
        this.areas = data.areas || [];
        this.slots = data.slots || [];
    }

    is(number) { return this.number === number; }
}

class Division {
    constructor(data) {
        this.id = data.id;
        this.number = data.number;
        this.name = data.name;
        this.bracketType = data.bracketType;
        this.loserBracket = data.loserBracket;
        this.games = data.games.map(game => new Game(game));
        this.selectedGame = data.selectedGame;
    }

    getGame(number) {
        return this.games.find(game => game.is(number));
    }

    is(number) {
        return this.number === number; 
    }
}

class Game {
    constructor(data) {
        this.id = data.id;
        this.number = data.number;
        this.division = data.division;
        this.team1 = data.teamRed;
        this.team2 = data.teamBlue;
        this.parents = data.parents; 
        this.children = data.children; 
        this.losersBracket = data.losersBracket;

        this.pending = data.pending;
        this.completed = data.completed;
        this.winner = data.winner; 

        this.sheet = data.site;
        this.col = data.area;
        this.row = data.slot;
    }


    set(sheet, col, row) {
        this.sheet = sheet;
        this.col = col;
        this.row = row;
        if (!isAValue(this.sheet) && !isAValue(this.col) && !isAValue(this.row)) {
            console.warn('Game is not assigned');
        }
    }

    clear() {
        if (!this.is_assigned()) {
            console.warn('Game is not assigned');
        }
        this.sheet = null;
        this.col = null;
        this.row = null;
    }

    is(number) { return this.number === number; }

    is_assigned() { return isAValue(this.sheet) }

    cellContent() { return `Division ${this.division}-${this.number}`; }
}


class TableElements {
    static _prependRow(tr, textContent) {
        let th = document.createElement('th');
        th.textContent = textContent;
        tr.prepend(th);
    }

    static getTd(row, col) {
        const td = document.createElement('td');
        td.dataset.row = row;
        td.dataset.col = col;
        td.setAttribute('draggable', true);
        return td;
    }

    static getTr(width, row) {
        const tr = document.createElement('tr');
        for (let col = 0; col < width ; col++) {
            tr.appendChild(this.getTd(row, col));
        }
        return tr;
    }

    static getThead(headerLabels) {
        const thead = document.createElement('thead');
        const tr = document.createElement('tr');
        headerLabels.forEach(label => {
            const th = document.createElement('th');
            th.textContent = label;
            tr.appendChild(th);
        });
        this._prependRow(tr, 'Time');
        thead.appendChild(tr);
        return thead;
    }


    static getTbody(rowLabels, width) {
        const tbody = document.createElement('tbody');
        rowLabels.forEach((label, row) => {
            let tr = this.getTr(width, row);
            this._prependRow(tr, label);
            tbody.appendChild(tr);
        });
        return tbody;
    }

    static newTable(sheet) {
        return {
            thead: TableElements.getThead(sheet.colLabels, sheet.height),
            tbody: TableElements.getTbody(sheet.rowLabels, sheet.width)
        }
    }

}

class ControlsUi {
    ids = {
        buttons: { save: 'saveButton', reset: 'resetButton', },
        inputs: { loserBracket: 'loserBracketInput', },
        select: {
            division: 'divisionSelect',
            site: 'siteSelect',
            bracketType: 'bracketTypeSelect', 
        },
    }

    bracketTypes = [ 
        { id: 0, name: "Single Elimination" }, 
        { id: 1, name: "Double Elimination" },
        { id: 2, name: "Round Robin" },
    ];

    constructor() {
        this.saveButton = document.getElementById(this.ids.buttons.save);
        this.resetButton = document.getElementById(this.ids.buttons.reset);
        this.loserBracketInput = document.getElementById(this.ids.inputs.loserBracket);
        this.divisionSelect = document.getElementById(this.ids.select.division);
        this.siteSelect = document.getElementById(this.ids.select.site);
        this.bracketTypeSelect = document.getElementById(this.ids.select.bracketType);
    }
}

class GameUi {
    id = { games: 'gamesContainer' }

    constructor() {
        this.elm = document.getElementById(this.id.games);
    }

    create(game) {
        console.log(game);
        const div = document.createElement('div');
        this._addBaseStyles(game, div);
        this._addBaseData(game, div);
        this._setAttributes(game, div);
        this._appendElement(div);
    }

    getElement(number) { 
        const elm = document.getElementById(`game-${number}`);
        if (!elm) { console.warn('Element not found', number); }
        return elm;
    }

    remove(number) {
        this.getElement(number).remove();
    }

    clear() {
        this.elm.innerHTML = '';
    }

// Base Setup
    _addBaseStyles(game, div) {
        div.classList.add(styles.game);
        if (game.pending) { div.classList.add(styles.pendingGame); }
        if (game.completed) { div.classList.add(styles.completedGame); }
    }

    _addBaseData(game, div) {
        div.innerHTML = game.cellContent();
        div.dataset.game = game.number;
        div.dataset.division = game.division;
    }

    _setAttributes(game, div) { 
        div.setAttribute('draggable', true);
        div.setAttribute('id', `game-${game.number}`);
    }

    _appendElement(div) {
        this.elm.appendChild(div);
    }


// Related Styles
    addRelatedStyles(number) {
        this.getElement(number).classList.add(styles.relatedGame); 
    }

    removeRelatedStyles(number) {
        this.getElement(number).classList.remove(styles.relatedGame); 
    }


// Selected Styles
    addSelectedElemStyles(number) {
        this.getElement(number).classList.add(styles.selectedGame); 
    }

    removeSelectedStyles(number) {
        this.getElement(number).classList.remove(styles.selectedGame); 
    }


// Member Styles
    addMemberStyles(number) {
        this.getElement(number).classList.add(styles.divisionMember); 
    }

    removeMemberStyles(number) {
        this.getElement(number).classList.remove(styles.divisionMember); 
    }

}

class Ui {
    id = { table: 'bracketBuilderTable' }

    constructor() {
        this.controls = new ControlsUi();
        this.gamesContainer = new GameUi();
        this.table = document.getElementById(this.id.table);
    }


    changeTable(table) {
        const thead = this.table.querySelector('thead');
        const tbody = this.table.querySelector('tbody');
        if (thead) { thead.replaceWith(table.thead); }
        else { this.table.prepend(table.thead); }
        if (tbody) { tbody.replaceWith(table.tbody); }
        else { this.table.appendChild(table.tbody); }
    }

    addGames(data) {
        data.unassigned.members.forEach(game => this.gamesContainer.create(game));
    }

    addStyles(data) {
        data.unassigned.members.forEach(game => this.gamesContainer.addMemberStyles(game.number));
        data.unassigned.parents.forEach(game => this.gamesContainer.addRelatedStyles(game.number));
        data.unassigned.children.forEach(game => this.gamesContainer.addRelatedStyles(game.number));
        if (!data.game.is_assigned()) { this.gamesContainer.addSelectedElemStyles(data.game.number); }
    }

    removeStyles(data) {
        
        data.unassigned.members.forEach(game => this.gamesContainer.removeMemberStyles(game.number));
        data.unassigned.parents.forEach(game => this.gamesContainer.removeRelatedStyles(game.number));
        data.unassigned.children.forEach(game => this.gamesContainer.removeRelatedStyles(game.number));
        if (!data.game.is_assigned()) { this.gamesContainer.removeSelectedStyles(data.game.number); }
    }

}

class TableManager {
    constructor(sheet) {
        const table = TableElements.newTable(sheet);
        this.tbody = table.tbody
        this.thead = table.thead
    }

    getElement(col, row) {
        return this.tbody.children[row].children[col + 1];
    }
// Member Styles
    addMemberStyles(col, row) {
        this.getElement(col, row).classList.add(styles.divisionMember);
    }

    removeMemberStyles(col, row) {
        this.getElement(col, row).classList.remove(styles.divisionMember); 
    }
// Selected Styles
    addSelectStyles(col, row) {
        this.getElement(col, row).classList.add(styles.selectedGame);
    }

    removeSelectStyles(col, row) {
        this.getElement(col, row).classList.remove(styles.selectedGame);
    }
// Related Styles
    addRelatedStyles(col, row) {
        this.getElement(col, row).classList.add(styles.relatedGame); 
    }

    removeRelatedStyles(col, row) {
        this.getElement(col, row).classList.remove(styles.relatedGame); 
    }

    addStyles(data) {
        data.members.forEach(game => this.addMemberStyles(game.col, game.row));
        data.parents.forEach(game => this.addRelatedStyles(game.col, game.row));
        data.children.forEach(game => this.addRelatedStyles(game.col, game.row));
        if (data.game) { this.addSelectStyles(data.game.col, data.game.row); }
    }

    removeStyles(data) {
        data.members.forEach(game => this.removeMemberStyles(game.col, game.row));
        data.parents.forEach(game => this.removeRelatedStyles(game.col, game.row));
        data.children.forEach(game => this.removeRelatedStyles(game.col, game.row));
        if (data.game) { this.removeSelectStyles(data.game.col, data.game.row); }
    }

    setCell(game) {
        const cell = this.getElement(game.col, game.row);
        cell.innerHTML = game.cellContent();
        cell.dataset.game = game.number;
        cell.dataset.division = game.division;
        cell.classList.add(styles.game);
        if (game.pending) { cell.classList.add(styles.pendingGame); }
        if (game.completed) { cell.classList.add(styles.completedGame); }
    }

    clearCell(col, row) {
        const cell = this.getElement(col, row);
        cell.innerHTML = '';
        cell.dataset.game = '';
        cell.dataset.division = '';
        cell.classList.remove(styles.game);
    }

    blockRows(limits) {
        let highLimit = limits.highLimit;
        let lowLimit = limits.lowLimit;

        if (!isAValue(highLimit)) {
            highLimit = -1
        }

        if (!isAValue(lowLimit)) {
            lowLimit = this.tbody.children.length;
        }

        for (let i = 0; i < this.tbody.children.length; i++) {
            const row = this.tbody.children[i];

            if (i < highLimit || i > lowLimit) {

                for (const cell of row.children) {
                    cell.classList.add('blocked');
                }

            } else {
                for (const cell of row.children) {
                    cell.classList.remove('blocked');
                }
            }
        }
    }

}

class Sheet {
    constructor(data) {
        this.id = data.id;
        this.index = data.index;
        this.name = data.name;
        this.height = data.height;
        this.width = data.width;
        this.colLabels = data.colLabels;
        this.rowLabels = data.rowLabels;
        this.data = this._initData();
        this.table = new TableManager(this);
        this.changeQueue = [];
    }

    _initData() {
        return Array.from({ length: this.height }, () => Array(this.width).fill(null));
    }

    getCell(col, row) { 
        return this.data[row][col];
    }

    setCell(col, row, game) {
        game.set(this.index, col, row);
        this.data[row][col] = game;
        this.table.setCell(game);
    }

    clearCell(col ,row) {
        const game = this.getCell(col, row);
        if (!game) { return; }
        game.clear();
        this.data[row][col] = null;
        this.table.clearCell(col, row);
    }

    gameSetMatch(data) {
        if (!data.game) { return null; }
        if (!data.game.is_assigned()) { return null;}
        if (data.game.sheet !== this.index) { return null; }
        return data.game;
    }

    filterData(data) {
        return {
            game: this.gameSetMatch(data),
            members: data.assigned.members.filter(game => game.sheet === this.index),
            parents: data.assigned.parents.filter(game => game.sheet === this.index),
            children: data.assigned.children.filter(game => game.sheet === this.index),
        };
    }

    removeStyles(data) {
        this.table.removeStyles(this.filterData(data));
    }

    addStyles(data) {
        this.table.addStyles(this.filterData(data));
    }

}

class Sheets {
    constructor() {
        this.sheetData = [];
    }

    addSheet(sheet) {
        this.sheetData.push(sheet); 
    }

    setCell(index, col, row, game) {
        this.sheetData[index].setCell(col, row, game);
    }

    getCell(index, col, row) {
        return this.sheetData[index].getCell(col, row) ;
    }

    clearCell(index, col, row) {
        this.sheetData[index].clearCell(col, row);

    }

    addStyles(data) {
        this.sheetData.forEach(sheet => sheet.addStyles(data));
    }

    removeStyles(data) {
        this.sheetData.forEach(sheet => sheet.removeStyles(data));
    }

}


class DivisionManager {
    constructor(divisions) {
        this.data = divisions;
    }

    get(number) {
        return this.data.find(division => division.is(number));
    }

    getData(number) {
        const division = this.get(number);
        const game = division.getGame(division.selectedGame);
        return {
            game: game,
            assigned: {
                members: division.games.filter(game => game.is_assigned()),
                parents: game.parents.map(parent => division.getGame(parent))
                    .filter(game => game.is_assigned()),
                children: game.children.map(child => division.getGame(child))
                    .filter(game => game.is_assigned()),
            },
            unassigned: {
                members: division.games.filter(game => !game.is_assigned()),
                parents: game.parents.map(parent => division.getGame(parent))
                    .filter(game => !game.is_assigned()),
                children: game.children.map(child => division.getGame(child))
                    .filter(game => !game.is_assigned()),
            },
        };
    }

    getFirstParentRow(game) {
        const division = this.get(game.division)
        const parents = game.parents
            .map(parent => division.getGame(parent))
            .filter(parent => parent && parent.is_assigned());
        
        if (parents.length === 0) { return null; }
        const rows = parents.map(parent => parent.row);
        return Math.max(...rows) + 1;
    }

    getLastChildRow(game) {
        const division = this.get(game.division)
        const children = game.children
            .map(child => division.getGame(child))
            .filter(child => child && child.is_assigned());

        if (children.length === 0) { return null; }
        const rows = children.map(child => child.row);
        return Math.min(...rows) - 1;
    }

}

class State {

    constructor(data) {
        this.sheets = data.sheets;
        this.divisions = data.divisions;
        this.activesheet = data.activeSheet || 0;
        this.activeDivision = data.activeDivision || 1;
    }

    getTable() {
        return this.sheets.sheetData[this.activeSheet].table;
    }

    getGames() {
        return this.divisions.getData(this.activeDivision);
    }

    blockUnassignable(game) {
        const limits = {
            highLimit: this.divisions.getFirstParentRow(game),
            lowLimit: this.divisions.getLastChildRow(game),
        };
        this.sheets.sheetData.forEach(sheet => sheet.table.blockRows(limits));
    }

}

class BracketBuilder {
    constructor() {
        const sites = Ajax.fetchSites();
        const divisions = Ajax.fetchDivisions();
        this.state = initState(sites, divisions);
        this.ui = initUi(sites, divisions);
        this._init();
        this.openContextMenu = null;
        this.openTooltip = null;
        this.selectedGame = null;
    }

    _getGame(e) {
        if (e.target.dataset.game && e.target.dataset.division) {
            this._clearTable();
            this.ui.gamesContainer.clear();

            const game = this.state.divisions.get(Number(e.target.dataset.division))
                .getGame(Number(e.target.dataset.game));
            this.state.activeDivision = game.division;
            this.state.divisions.get(game.division).selectedGame = game.number;
            this.selectedGame = game;



            this.ui.addGames(this.state.getGames());
            this._updateTable();
            return game;
        }
        return null;
    }

    _clearTable() {
        const data = this.state.getGames();
        this.state.sheets.removeStyles(data);
        this.ui.removeStyles(data);
        this.state.sheets.sheetData.forEach(sheet => sheet.table.blockRows({}));
    }

    _updateTable() {
        const data = this.state.getGames();
        this.ui.addStyles(data);
        this.ui.controls.divisionSelect.value = data.game.division; // Come back and check if data.game is null
        this.state.sheets.addStyles(data);
        this.ui.changeTable(this.state.getTable());
        this.state.blockUnassignable(data.game);
    }

    _siteSelectChange(e) {
        this._clearTable();
        this.state.activeSheet = Number(e.target.value);
        this._updateTable();
    }

    _divisionsSelectChange(e) {
        this._clearTable();
        this.ui.gamesContainer.clear();
        this.state.activeDivision = Number(e.target.value);
        this.ui.addGames(this.state.getGames());
        this._updateTable();
    }

    _closeTooltip() {
        if (this.openTooltip) {
            this.openTooltip.remove();
            this.openTooltip = null;
        }
    }

    _renderTootip(game, x, y) {
        this._closeTooltip();
        const tableContainer = document.getElementById('tableContainer');
        const tooltip = document.createElement('div');
        tooltip.innerHTML = `
            <h4>${game.team1} vs ${game.team1}</h4>
            <p>Game: ${game.number}</p>
            <p>Division: ${game.division}</p>
            <p>Site: ${game.sheet}</p>
            <p>Area: ${game.col + 1}</p>
            <p>Slot: ${game.row + 1}</p>
        `
        tooltip.style.position = 'fixed';
        tooltip.style.top = `${y}px`;
        tooltip.style.left = `${x}px`;
        tooltip.classList.add('sheet-table__tooltip');
        tooltip.setAttribute('id', 'tooltip');
        tableContainer.appendChild(tooltip);
        this.openTooltip = tooltip;
    }

    _closeContextMenu() {
        if (this.openContextMenu) {
            this.openContextMenu.remove();
            this.openContextMenu = null;
        }
    }

    _renderContextMenu(game, x, y) {
        this._closeContextMenu();
        const tableContainer = document.getElementById('tableContainer');
        const contextMenu = document.createElement('div');
        contextMenu.innerHTML = `
            <button class="btn">edit</button>
            <button class="btn">remove</button>
            <button class="btn">close</button>
        `
        contextMenu.style.position = 'fixed';
        contextMenu.style.top = `${y}px`;
        contextMenu.style.left = `${x}px`;
        contextMenu.classList.add('sheet-table__tooltip');
        contextMenu.setAttribute('id', 'contextMenu');
        tableContainer.appendChild(contextMenu);
        this.openContextMenu = contextMenu;
    }

    _getCoords(e) {
        let coords = { 
            x: e.clientX,
            y: e.clientY,
        };

        let offsetX = coords.x + 200 - window.innerWidth;
        if (offsetX > 0) {
            coords.x -= offsetX + 10; 
        }
        let offsetY = coords.y + 100 - window.innerHeight;
        if (offsetY > 0) {
            coords.y -= offsetY + 10;
        }
        return coords;
    }

    _clickWithGames(e) {
        this._getGame(e);
    }

    _clickEmptyCell(e) {
        this._clearTable();
        this.state.selectedDivision = null;
    }

    _contextMenuClick(e) {
        this._closeContextMenu();
    }

    _cellClick(e) {
        if (e.target.dataset.game && e.target.dataset.division) {
            this._clickWithGames(e);
            return
        } 
        this._clickEmptyCell(e);
    }

    click(e) {
        this._closeTooltip();
        if (e.target == this.openContextMenu) {
            this._contextMenuClick(e);
            return;
        }
        this._closeContextMenu();
        if (e.target.tagName == 'TD') {
            this._cellClick(e);
            return;
        } 


    }

    contextMenu(e) {
        const game = this._getGame(e);
        if (!game) { return; }
        this._closeContextMenu();
        this._closeTooltip();
        e.preventDefault();
        const coords = this._getCoords(e);
        this._renderContextMenu(game, coords.x, coords.y);
    }

    dbClick(e) {
        const game = this._getGame(e);
        if (!game) { return; }

        const coords = this._getCoords(e);
        this._renderTootip(game, coords.x, coords.y);
    }

    dragStart(e) {
        const game = this._getGame(e);
        if (!game) { return; }
        this.selectedGame = game;
    }

    dragOver(e) {
        e.preventDefault();
        if (e.target.dataset.col && e.target.dataset.row) {
            if (e.target.tagName !== 'TD') { return; }
            if (e.target.classList.contains('blocked')) { return; }
            e.target.classList.add('drag-over');
        }
    }

    dragLeave(e) {
        e.preventDefault();
        if (e.target.tagName !== 'TD') { return; }
        e.target.classList.remove('drag-over');
    }

    dragEnd(e) {
        e.target.classList.remove('drag-over');
        this.selectedGame = null;
    }
    
    dragDrop(e) {
        e.preventDefault();
        const game = this.selectedGame;
        if (!game) { return; }
        if (e.target.tagName !== 'TD') { return; }
        if (e.target.dataset.game && e.target.dataset.division) { return; }
        if (e.target.classList.contains('blocked')) { return; }
        const sheet = game.sheet;
        const col = Number(e.target.dataset.col);
        const row = Number(e.target.dataset.row);

        this._clearTable();
        this.state.sheets.clearCell(sheet, game.col, game.row);
        this.state.sheets.setCell(sheet, col, row, game);
        this._updateTable();
    }

    _tableListeners() {
        this.ui.table.addEventListener('click', e => { this.click(e); });
        this.ui.table.addEventListener('dblclick', e => { this.dbClick(e); });
        this.ui.table.addEventListener('contextmenu', e => { this.contextMenu(e); });
        this.ui.table.addEventListener('dragstart', e => { this.dragStart(e); });
        this.ui.table.addEventListener('dragover', e => { this.dragOver(e); });
        this.ui.table.addEventListener('dragend', e => { this.dragEnd(e); });
        this.ui.table.addEventListener('dragleave', e => { this.dragLeave(e); });
        this.ui.table.addEventListener('drop', e => { this.dragDrop(e); });
    }

    _containerClick(e) {
        this._getGame(e);
    }

    _gameContainerListeners() {
        this.ui.gamesContainer.elm.addEventListener('click', e => { this._containerClick(e); });
    }

    _controlListeners() {
        this.ui.controls.siteSelect.addEventListener('change', e => { this._siteSelectChange(e); });
        this.ui.controls.divisionSelect.addEventListener('change', e => { this._divisionsSelectChange(e); });
    }

    _init() {
        this._tableListeners();
        this._gameContainerListeners();
        this._controlListeners();

    }

}

function initState(sites, divisions) {
    return new State({
        sheets: initSheets(sites, divisions),
        divisions: new DivisionManager(divisions),
        active: 0,
    });
}

function initSheets(sites, divisions, ) {
    const sheets = new Sheets();
    sites.forEach((site, index) => {
        sheets.addSheet(new Sheet( 
            {
                id: site.id,
                index: index,
                name: site.name,
                height: site.slots.length,
                width: site.areas.length,
                colLabels: site.areas,
                rowLabels: site.slots,
            }),
        );
    });
    divisions.forEach(division => { 
        division.games.forEach(game => {
            if (game.is_assigned()) {
                sheets.setCell(game.sheet, game.col, game.row,  game);
            }
        });
    });
    return sheets;
}

function initUi(sites, divisions) {
    const ui = new Ui();
    sites.forEach((site, index) => {
        const option = document.createElement('option');
        option.value = index;
        option.text = `${site.name} - ${index}`;
        ui.controls.siteSelect.appendChild(option);
    });
    divisions.forEach(division => {
        const option = document.createElement('option');
        option.value = division.number;
        option.text = `${division.name} - ${division.number}`;
        ui.controls.divisionSelect.appendChild(option);
    });
    ui.controls.bracketTypes.forEach(bracketType => {
        const option = document.createElement('option');
        option.value = bracketType.number;
        option.text = bracketType.name;
        ui.controls.bracketTypeSelect.appendChild(option);
    });
    return ui;

}

function isAValue(value) { return value !== null && value !== undefined; }


document.addEventListener('DOMContentLoaded', () => {
    new BracketBuilder();
    document.getElementById('bracketOpenButton').addEventListener('click', () => {
        document.getElementById('bracketBuilderOverlay').classList.toggle('show');
    });
    document.getElementById('closeBracketBuilderButton').addEventListener('click', () => {
        document.getElementById('bracketBuilderOverlay').classList.remove('show');
    });
});
