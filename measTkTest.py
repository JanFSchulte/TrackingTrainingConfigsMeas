import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run2_2017_cff import Run2_2017
process = cms.Process("TEST",Run2_2017)

process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')
process.GlobalTag = GlobalTag(process.GlobalTag,'auto:phase1_2017_realistic', '')
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic', '')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
# needed if not reading events
process.VolumeBasedMagneticFieldESProducer.valueOverride = 18000


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        '/store/mc/Run3Summer19DR/TTbar_14TeV_TuneCP5_Pythia8/GEN-SIM-DIGI-RAW/106X_mcRun3_2024_realistic_v4-v2/270000/E47142AC-1C40-C04B-B489-67A0F21F8F58.root', 
        
    ),
    secondaryFileNames = cms.untracked.vstring()
)

process.siPixelDigis = cms.EDProducer("SiPixelRawToDigi", 
    CablingMapLabel = cms.string(''), 
    ErrorList = cms.vint32(29), 
    IncludeErrors = cms.bool(True), 
    InputLabel = cms.InputTag("rawDataCollector"), 
    Regions = cms.PSet( 
 
    ), 
    Timing = cms.untracked.bool(False), 
    UsePhase1 = cms.bool(True), 
    UsePilotBlade = cms.bool(False), 
    UseQualityInfo = cms.bool(False), 
    UserErrorList = cms.vint32(40) 
) 

process.siPixelClusters = cms.EDProducer("SiPixelClusterProducer", 
    ChannelThreshold = cms.int32(10), 
    ClusterMode = cms.string('PixelThresholdClusterizer'), 
    ClusterThreshold = cms.int32(4000), 
    ClusterThreshold_L1 = cms.int32(2000), 
    ElectronPerADCGain = cms.double(135), 
    MissCalibrate = cms.bool(True), 
    Phase2Calibration = cms.bool(False), 
    Phase2DigiBaseline = cms.double(1200), 
    Phase2KinkADC = cms.int32(8), 
    Phase2ReadoutMode = cms.int32(-1), 
    SeedThreshold = cms.int32(1000), 
    SplitClusters = cms.bool(False), 
    VCaltoElectronGain = cms.int32(47), 
    VCaltoElectronGain_L1 = cms.int32(50), 
    VCaltoElectronOffset = cms.int32(-60), 
    VCaltoElectronOffset_L1 = cms.int32(-670), 
    maxNumberOfClusters = cms.int32(-1), 
    payloadType = cms.string('Offline'), 
    src = cms.InputTag("siPixelDigis") 
) 


process.MeasurementTrackerEvent = cms.EDProducer("MeasurementTrackerEventProducer",
    Phase2TrackerCluster1DProducer = cms.string(''),
    badPixelFEDChannelCollectionLabels = cms.VInputTag("siPixelDigis"),
    inactivePixelDetectorLabels = cms.VInputTag("siPixelDigis"),
    inactiveStripDetectorLabels = cms.VInputTag("siStripDigis"),
    measurementTracker = cms.string(''),
    pixelCablingMapLabel = cms.string(''),
    pixelClusterProducer = cms.string('siPixelClusters'),
    skipClusters = cms.InputTag(""),
    stripClusterProducer = cms.string('siStripClusters'),
    switchOffPixelsIfEmpty = cms.bool(True)
)

process.SiStripClusterChargeCutNone = cms.PSet(
    value = cms.double(-1.0)
)


process.siStripClusters = cms.EDProducer("SiStripClusterizer",
    Clusterizer = cms.PSet(
        Algorithm = cms.string('ThreeThresholdAlgorithm'),
        ChannelThreshold = cms.double(2.0),
        ClusterThreshold = cms.double(5.0),
        MaxAdjacentBad = cms.uint32(0),
        MaxSequentialBad = cms.uint32(1),
        MaxSequentialHoles = cms.uint32(0),
        QualityLabel = cms.string(''),
        RemoveApvShots = cms.bool(True),
        SeedThreshold = cms.double(3.0),
        clusterChargeCut = cms.PSet(
            refToPSet_ = cms.string('SiStripClusterChargeCutNone')
        )
    ),
    DigiProducersList = cms.VInputTag(cms.InputTag("siStripDigis","ZeroSuppressed"), cms.InputTag("siStripZeroSuppression","VirginRaw"), cms.InputTag("siStripZeroSuppression","ProcessedRaw"), cms.InputTag("siStripZeroSuppression","ScopeMode"))
)


process.siStripDigis = cms.EDProducer("SiStripRawToDigiModule",
    AppendedBytes = cms.int32(0),
    DoAPVEmulatorCheck = cms.bool(False),
    DoAllCorruptBufferChecks = cms.bool(False),
    ErrorThreshold = cms.uint32(7174),
    LegacyUnpacker = cms.bool(False),
    MarkModulesOnMissingFeds = cms.bool(True),
    ProductLabel = cms.InputTag("rawDataCollector"),
    TriggerFedId = cms.int32(0),
    UnpackBadChannels = cms.bool(False),
    UnpackCommonModeValues = cms.bool(False),
    UseDaqRegister = cms.bool(False),
    UseFedKey = cms.bool(False)
)

process.scalersRawToDigi = cms.EDProducer("ScalersRawToDigi", 
    scalersInputTag = cms.InputTag("rawDataCollector") 
)


process.myTest  = cms.EDAnalyzer("MeasurementTrackerTest",
 measurementTracker = cms.string(''),
 navigationSchool   = cms.string('SimpleNavigationSchool'),
 MeasurementTrackerEvent = cms.InputTag("MeasurementTrackerEvent") 
)



process.p1 = cms.Path(process.scalersRawToDigi*process.siPixelDigis*process.siPixelClusters*process.siStripDigis*process.siStripClusters*process.MeasurementTrackerEvent*process.myTest)

