;(function (root, factory) {
    typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory() :
        typeof define === 'function' && define.amd ? define(factory) :
            root.ui = factory();
}(this, function () {
    /**
     * @module Dialog Class
     */
    class Dialog {

        /**
         *
         * @param modal bootstrap modal
         */
        constructor(modal) {
            this.modal = modal;

            let isAnotherModalShow = false;
            $(`#${this.modal.id}`).on('show.bs.modal', () => {
                isAnotherModalShow = document.getElementsByTagName('body')[0].classList.contains('modal-open');
            });

            $(`#${this.modal.id}`).on('hidden.bs.modal', () => {
                if (isAnotherModalShow) {
                    document.getElementsByTagName('body')[0].classList.add('modal-open');
                }
                document.getElementById(this.modal.id).remove();
            });
        }

        /**
         * build dialog,
         * setMessage [recommend required]
         * setTitle [optional]
         * addConfirmButton [recommend required]
         * addCancelButton [optional] if you need cancel button, usually applied in confirm style dialog
         * @type {*}
         */
        static Builder = class {
            constructor() {
                const modal = document.createElement('div');
                modal.className = 'modal fade';
                modal.id = this.uuid();
                modal.setAttribute('tabindex', '-1');
                modal.setAttribute('aria-labelledby', 'dialogModalLabel');
                modal.setAttribute('aria-hidden', 'true');
                modal.setAttribute('data-backdrop', 'static');

                const modalDialog = document.createElement('div');
                modalDialog.className = 'modal-dialog modal-dialog-centered';

                const modalContent = document.createElement('div');
                modalContent.className = 'modal-content';

                const modalHeader = document.createElement('div');
                modalHeader.className = 'modal-header border-0';

                const modalFooter = document.createElement('div');
                modalFooter.className = 'modal-footer border-0';

                const modalTitle = document.createElement('h6');
                modalTitle.className = 'modal-title';

                const modalBody = document.createElement('div');
                modalBody.className = 'modal-body';

                this.modal = modal;
                this.modalHeader = modalHeader;
                this.modalTitle = modalTitle;
                this.modalBody = modalBody;
                this.modalDialog = modalDialog;
                this.modalContent = modalContent;
                this.modalFooter = modalFooter;
            }

            setMessage(message) {
                this.modalBody.innerText = message || '';
                return this;
            }

            setTitle(title) {
                this.modalTitle.innerText = title || '';
                return this;
            }

            addConfirmButton() {
                const confirmButton = document.createElement('button');
                confirmButton.id = `${this.modal.id}-confirm`;
                confirmButton.className = 'btn text-primary';
                confirmButton.textContent = '確定';
                confirmButton.setAttribute('data-bs-dismiss', 'modal');
                this.confirmButton = confirmButton;

                return this;
            }

            addCancelButton() {
                const cancelButton = document.createElement('button');
                cancelButton.id = `${this.modal.id}-cancel`;
                cancelButton.className = 'btn text-primary';
                cancelButton.textContent = '取消';
                cancelButton.setAttribute('data-bs-dismiss', 'modal');
                this.cancelButton = cancelButton;

                return this;
            }

            addInteractive(defaultValue, placeholder, pattern) {
                const interactiveInput = document.createElement('input');
                interactiveInput.id = `${this.modal.id}-input`;
                interactiveInput.className = 'form-control w-50 d-flex align-self-center';
                interactiveInput.placeholder = placeholder || '';
                interactiveInput.pattern = pattern || '';
                interactiveInput.value = defaultValue || '';
                this.interactiveInput = interactiveInput;

                return this;
            }

            uuid() {
                let d = Date.now();
                if (typeof performance !== 'undefined' && typeof performance.now === 'function') {
                    d += performance.now(); // use high-precision timer if available
                }
                return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
                    const r = (d + window.crypto.getRandomValues(new Uint32Array(1))[0] * 16) % 16 | 0;
                    d = Math.floor(d / 16);
                    return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
                });
            }

            build() {
                this.modalHeader.appendChild(this.modalTitle);
                this.modalContent.appendChild(this.modalHeader);
                this.modalContent.appendChild(this.modalBody);
                if (this.confirmButton)
                    this.modalFooter.appendChild(this.confirmButton);
                if (this.cancelButton)
                    this.modalFooter.appendChild(this.cancelButton);
                if (this.interactiveInput)
                    this.modalContent.appendChild(this.interactiveInput);
                this.modalContent.appendChild(this.modalFooter);
                this.modalDialog.appendChild(this.modalContent);
                this.modal.appendChild(this.modalDialog);
                document.body.appendChild(this.modal);

                return new Dialog(this.modal);
            }
        }

        /**
         * display dialog
         * @returns {Dialog}
         */
        popup() {
            $(`#${this.modal.id}`).modal('show');
            return this;
        }

        /**
         * trigger when the confirm button onclick
         * @param callback this function is executed when user click **confirm** button
         * @returns {Dialog}
         */
        confirm(callback) {
            document.getElementById(`${this.modal.id}-confirm`).onclick = () => {
                callback(this);
            };
            return this;
        }

        /**
         * trigger when the confirm button onclick
         * @param callback this function is executed when user click **cancel** button
         * @returns {Dialog}
         */
        cancel(callback) {
            document.getElementById(`${this.modal.id}-cancel`).onclick = () => callback();
            return this;
        }

        /**
         * trigger when dialog displaying
         * @param callback this function is executed when dialog display
         * @returns {Dialog}
         */
        show(callback) {
            $(`#${this.modal.id}`)
                .on('show.bs.modal', () => {
                    if (typeof callback === 'function')
                        callback();
                });
            return this;
        }

        /**
         * trigger when dialog dismiss
         * @param callback this function is executed when dialog dismiss
         * @return {Dialog}
         */
        hide(callback) {
            $(`#${this.modal.id}`)
                .on('hide.bs.modal', () => {
                    if (typeof callback === 'function')
                        callback();
                });
            return this;
        }
    }

    class Loading {
        constructor() {
            const container = document.getElementById('wrapper') || document.body;
            const html = '<link rel="stylesheet" href="/statics/bower_components/chtsec-ui/ui.css"> <div class="block-container">  <div class="load-wrapp"> <div class="load-fade">     <div class="load-letter-holder">         <div class="load-letter-1 load-letter">L</div>         <div class="load-letter-2 load-letter">o</div>         <div class="load-letter-3 load-letter">a</div>         <div class="load-letter-4 load-letter">d</div>         <div class="load-letter-5 load-letter">i</div>         <div class="load-letter-6 load-letter">n</div>         <div class="load-letter-7 load-letter">g</div>         <div class="load-letter-8 load-letter">.</div>         <div class="load-letter-9 load-letter">.</div>         <div class="load-letter-10 load-letter">.</div>     </div> </div>  </div>  <div class="load-wrapp"> <div class="load-wave">     <div class="line"></div>     <div class="line"></div>     <div class="line"></div> </div>  </div>        </div>';
            let loadingDiv = document.createElement('div');
            loadingDiv.style.display = 'none';
            loadingDiv.innerHTML = html;
            container.appendChild(loadingDiv);

            this.loadingDiv = loadingDiv;
        }

        start() {
            this.loadingDiv.style.display = 'block';
        }

        stop() {
            this.loadingDiv.style.display = 'none';
        }
    }

    return {
        /**
         * simple way to create alert dialog
         * ui.alert('message', 'title');
         * @param message
         * @param title [Optional]
         * @returns {Dialog}
         */
        alert: (message, title) => new Dialog.Builder().setMessage(message).setTitle(title).addConfirmButton().build().popup(),

        /**
         * simply way to create confirm dialog
         * ui.dialog(message, title).confirm(() => {...})
         * @param message
         * @param title [Optional]
         * @returns {Dialog}
         */
        dialog: (message, title) => new Dialog.Builder().setMessage(message).setTitle(title).addConfirmButton().addCancelButton().build().popup(),

        /**
         * simply way to create confirm dialog
         * ui.prompt(message, title, placeholder, pattern).confirm(() => {...})
         * @param message
         * @param title [Optional]
         * @param defaultValue [Optional] input default value
         * @param placeholder [Optional] input placeholder attribute
         * @param pattern [Optional] input pattern, used to restrict user input
         * @returns {Dialog}
         */
        prompt: (message, title, defaultValue, placeholder, pattern) => new Dialog.Builder().setMessage(message).setTitle(title).addInteractive(defaultValue, placeholder, pattern).addConfirmButton().addCancelButton().build().popup(),
        Dialog: Dialog,
        Loading: new Loading()
    };
}));