from string import Template
from ..config import (hostname,
                     port,
                     username,
                     csr_bundle_style_css_dir as remote_svelte_bundle_dir 
                     )

from ..helper_utils import write_to_bundler_dir

setup_websocket_cjs = """
export class WebSocketManager {
    constructor(pageId, options = {}) {
        // Critical Configuration
        this.pageId = pageId;
        if (!this.pageId) {
            console.error("WebSocketManager: PAGE_ID is required.");
        }

        // Configurable Options
        this.debug = options.debug ?? true;
        this.staticResourcesUrl = options.staticResourcesUrl || '/static/';

        // Connection State
        this.socket = null;
        this.websocketId = null;
        this.websocketReady = false;
        this.webSocketClosed = false;
        this.pageReady = false;
        this.resultReady = true;

        // Reload State
        this.reloadStarted = false;
        this.reloadTimeout = 1000;

        // Outbound Message Queue
        this.messageQueue = [];

        // Auto-initialize connection
        this.initConnection();
    }

    initConnection() {
        const protocolString = 'wss://';
        let wsUrl = protocolString + document.domain;
        if (location.port) {
            wsUrl += ':' + location.port;
        }

        this.socket = new WebSocket(wsUrl);

        // Arrow functions natively preserve the class instance context (this)
        this.socket.addEventListener('open', () => {
            if (this.debug) console.log('WebSocket opened');
            this.sendToServer({ 'type': 'connect', 'page_id': this.pageId }, 'connect');
        });

        this.socket.addEventListener('error', (event) => {
            if (this.debug) console.error('WebSocket error:', event);
            this.reloadSite();
        });

        this.socket.addEventListener('close', () => {
            if (this.debug) console.log('WebSocket closed');
            this.webSocketClosed = true;
            this.reloadSite();
        });

        this.socket.addEventListener('message', (event) => this.handleMessageEvent(event));
    }

    handleMessageEvent(event) {
       console.log("websocket message recieved");
        try {
            const msg = JSON.parse(event.data);
            console.log("msg = ", msg);
            switch (msg.type) {
                case 'page_update':
                    this.handlePageUpdateEvent(msg);
                    break;
                case 'websocket_update':
                    this.handleWebsocketUpdateEvent(msg);
                    break;
                case 'run_javascript':
                    this.handleRunJavascriptEvent(msg);
                    break;
                default:
                    if (this.debug) {
                        console.warn(`Message type "${msg.type}" has no registered handler`);
                    }
            }
        } catch (err) {
            if (this.debug) console.error("Failed to parse incoming WS message:", err);
        }
    }

    handlePageUpdateEvent(msg) {
        const options = msg.page_options || {};

        if (options.redirect) {
            if (this.debug) console.log("Now redirecting page to: ", options.redirect);
            location.href = options.redirect;
            return;
        }
        if (options.open) {
            window.open(options.open, '_blank');
        }
        if (options.display_url !== undefined && options.display_url !== null) {
            window.history.pushState("", "", options.display_url);
        }
        if (options.title) {
            document.title = options.title;
        }
        if (options.favicon) {
            let link = document.querySelector("link[rel*='icon']") || document.createElement('link');
            link.type = 'image/x-icon';
            link.rel = 'shortcut icon';
            link.href = options.favicon.startsWith('http') 
                ? options.favicon 
                : `${this.staticResourcesUrl}${options.favicon}`;
                
            document.getElementsByTagName('head')[0].appendChild(link);
        }
    }

    handleWebsocketUpdateEvent(msg) {
        console.log("websocket update event recieved");
        this.websocketId = msg.data;
        this.websocketReady = true;

        this.flushMessageQueue();

        if (this.pageReady) {
            const e = {
                'event_type': 'page_ready',
                'visibility': document.visibilityState,
                'page_id': this.pageId,
                'websocket_id': this.websocketId
            };
            this.sendToServer(e, 'page_event');
        }
    }

    handleRunJavascriptEvent(msg) {
        const executeCode = () => {
            try {
                return Promise.resolve(eval(msg.data));
            } catch (error) {
                return Promise.reject(error);
            }
        };

        executeCode()
            .then((value) => {
                this.sendResult(value, msg);
            })
            .catch((error) => {
                this.handleError(error, msg);
            });
    }

    handleError(error, msg) {
        if (this.debug) {
            console.error("Error executing dynamic script:", error);
        }
        this.sendResult("Error in javascript", msg);
    }

    sendResult(jsResult, originalMsg) {
        if (!this.resultReady || !originalMsg?.send) return;

        const e = {
            'event_type': 'result_ready',
            'visibility': document.visibilityState,
            'page_id': this.pageId,
            'websocket_id': this.websocketId,
            'request_id': originalMsg.request_id,
            'result': jsResult 
        };
        this.sendToServer(e, 'page_event');
    }

    sendToServer(payload, eventType) {
        if (this.debug) {
            console.log('Preparing packet:', { 'type': eventType, 'event_data': payload });
        }

        if (this.webSocketClosed) {
            if (this.debug) console.warn('Abort send (WebSocket is closed) → reloading site');
            this.reloadSite();
            return;
        }

        const dataStr = JSON.stringify({ 
            'type': eventType, 
            'event_data': payload, 
            'csrftoken': 'somevalue' 
        });

        if (this.websocketReady && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(dataStr);
        } else {
            this.messageQueue.push(dataStr);
        }
    }

    flushMessageQueue() {
        while (this.messageQueue.length > 0 && this.socket.readyState === WebSocket.OPEN) {
            const dataStr = this.messageQueue.shift();
            this.socket.send(dataStr);
        }
    }

    tryReloadSite() {
        fetch(window.location.href)
            .then(() => {
                if (this.debug) console.log('Site Available, reloading...');
                window.location.reload();
            })
            .catch((error) => {
                if (this.debug) {
                    console.log(`Site unavailable (${error.message}), retrying in ${this.reloadTimeout}ms`);
                }
                setTimeout(() => this.tryReloadSite(), this.reloadTimeout);
                if (this.reloadTimeout < 60000) {
                    this.reloadTimeout += 1000;
                }
            });
    }

    reloadSite() {
        if (!this.reloadStarted) {
            if (this.debug) console.log("Reloading site sequence initialized...");
            this.reloadStarted = true;
            setTimeout(() => this.tryReloadSite(), this.reloadTimeout);
        }
    }
}

"""

def publish_websocket_manager():
    write_to_bundler_dir(setup_websocket_cjs , "src/websocket_manager.js",
                         target_bundler_dir = remote_svelte_bundle_dir
                         )
        

            
    pass






