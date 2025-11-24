module.exports = {
  preset: 'ts-jest/presets/default-esm',
  testEnvironment: 'node',
  roots: ['<rootDir>/tests'],
  extensionsToTreatAsEsm: ['.ts'],
  moduleNameMapper: {
    '^(.*)\\.(yaml)$': '<rootDir>/tests/__mocks__/fileMock.js'
  },
  transform: {
    '^.+\\.(ts|js)$': ['ts-jest', { useESM: true, tsconfig: 'tsconfig.json' }]
  },
  globals: {
    'ts-jest': {
      useESM: true,
      isolatedModules: true
    }
  }
};
