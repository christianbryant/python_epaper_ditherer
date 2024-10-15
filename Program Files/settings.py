class ProgramSettings:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProgramSettings, cls).__new__(cls)
            cls._instance._inputfolder = "None"
            cls._instance._outputfolder = "None"
            cls._instance._rotate = False
            cls._instance._preview = False
            cls._instance._fit = False
            cls._instance._debug = False
        return cls._instance
    
    def get_inputfolder(self):
        return self._inputfolder
    
    def set_inputfolder(self, value):
        self._inputfolder = value

    def get_outputfolder(self):
        return self._outputfolder
    
    def set_outputfolder(self, value):
        self._outputfolder = value
    
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