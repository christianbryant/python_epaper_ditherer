class ProgramSettings:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProgramSettings, cls).__new__(cls)
            cls._instance._inputfolder = "None"
            cls._instance._outputfolder = "None"
            cls._instance._masterframe = None
            cls._instance._debugframe = None
            cls._instance._previewframe = None
            cls._instance._rotate = False
            cls._instance._preview = False
            cls._instance._fit = False
            cls._instance._debug = False
            cls._instance._displaysize = ()
            cls._instance._dithered_preview = []
        return cls._instance
    
    def get_inputfolder(self):
        return self._inputfolder
    
    def set_inputfolder(self, value):
        self._inputfolder = value

    def get_outputfolder(self):
        return self._outputfolder
    
    def set_outputfolder(self, value):
        self._outputfolder = value

    def get_masterframe(self):
        return self._masterframe
    
    def set_masterframe(self, value):
        self._masterframe = value

    def get_debugframe(self):
        return self._debugframe
    
    def set_debugframe(self, value):
        self._debugframe = value

    def get_previewframe(self):
        return self._previewframe
    
    def set_previewframe(self, value):
        self._previewframe = value

    def set_displaysize(self, value):
        self._displaysize = value

    def get_displaysize(self):
        return self._displaysize

    def set_dithered_preview(self, value):
        self._dithered_preview = value

    def get_dithered_preview(self):
        return self._dithered_preview
    
    def get_rotate(self):
        return self._rotate
    
    def set_rotate(self, value):
        self._rotate = value

    def get_preview(self):
        return self._preview
    
    def set_preview(self, value):
        self._preview = value

    def get_fit(self):
        return self._fit
    
    def set_fit(self, value):
        self._fit = value

    def get_debug(self):
        return self._debug
    
    def set_debug(self, value):
        self._debug = value